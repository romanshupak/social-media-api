from django.utils.dateparse import parse_datetime
from rest_framework import filters, status
from rest_framework.exceptions import PermissionDenied

from media_api.tasks import create_scheduled_post

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from media_api.models import Post, Comment, Like
from media_api.serializers import (
    PostSerializer,
    CommentSerializer,
    LikeSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author").prefetch_related(
        "comments", "likes"
    )
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["content"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != self.request.user:
            raise PermissionDenied("You are allowed to edit only yours posts")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != self.request.user:
            raise PermissionDenied(
                "You are allowed to delete only yours posts"
            )
        return super().destroy(request, *args, **kwargs)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated]
    )
    def my_posts(self, request):
        """Retrieve all posts of current user"""
        posts = (
            Post.objects.filter(author=request.user)
            .select_related("author")
            .prefetch_related("comments", "likes")
        )
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated]
    )
    def following_posts(self, request):
        """Retrieve all posts of users they are following"""
        following_users = request.user.following.all()
        posts = (
            Post.objects.filter(author__in=following_users)
            .select_related("author")
            .prefetch_related("comments", "likes")
        )
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["POST"],
        permission_classes=[IsAuthenticated]
    )
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if Like.objects.filter(post=post, user=user).exists():
            return Response(
                {"error": "Post already liked"},
                status=status.HTTP_400_BAD_REQUEST
            )
        Like.objects.create(post=post, user=user)
        return Response(
            {"message": "Post liked successfully"},
            status=status.HTTP_201_CREATED
        )

    @action(
        detail=True,
        methods=["POST"],
        permission_classes=[IsAuthenticated]
    )
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user
        like = Like.objects.filter(post=post, user=user).first()
        if not like:
            return Response(
                {"error": "Post not liked"},
                status=status.HTTP_400_BAD_REQUEST
            )
        like.delete()
        return Response(
            {"message": "Post unliked successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=["GET"])
    def liked_posts(self, request):
        user = request.user
        liked_posts = Post.objects.filter(likes__user=user)
        serializer = self.get_serializer(liked_posts, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["POST"],
        url_path="add-comment",
    )
    def create_comment(self, request, pk=None):
        """Create a comment for a specific post"""
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["GET"])
    def comments(self, request, pk=None):
        """Retrieve all comments for a specific post"""
        post = self.get_object()
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[IsAuthenticated]
    )
    def schedule_post(self, request):
        """Schedule creation of post"""
        content = request.data.get("content")
        scheduled_time_str = request.data.get("scheduled_time")

        # Перетворення рядка в datetime
        scheduled_time = parse_datetime(scheduled_time_str)

        if not content or not scheduled_time:
            return Response(
                {
                    "error": "It is necessary to fill out "
                    "content and time of scheduled post"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Планування завдання
        create_scheduled_post.apply_async(
            (content, request.user.id, scheduled_time), eta=scheduled_time
        )

        return Response(
            {"message": "Post will be created in scheduled time"},
            status=status.HTTP_202_ACCEPTED,
        )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().select_related("author", "post")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            raise PermissionDenied(
                "You are allowed to edit only yours comments"
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            raise PermissionDenied(
                "You are allowed to delete only yours comments"
            )
        return super().destroy(request, *args, **kwargs)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.select_related("user", "post")
    serializer_class = LikeSerializer
