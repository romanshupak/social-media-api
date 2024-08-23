from rest_framework import filters, status

from django.shortcuts import render
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
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["content"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def my_posts(self, request):
        """Retrieve all posts of current user"""
        posts = Post.objects.filter(author=request.user)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def following_posts(self, request):
        """Retrieve all posts of users they are following"""
        following_users = request.user.following.all()
        posts = Post.objects.filter(author__in=following_users)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if Like.objects.filter(post=post, user=user).exists():
            return Response(
                {"error": "Post already liked"}, status=status.HTTP_400_BAD_REQUEST
            )
        Like.objects.create(post=post, user=user)
        return Response(
            {"message": "Post liked successfully"}, status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["POST"])
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user
        like = Like.objects.filter(post=post, user=user).first()
        if not like:
            return Response(
                {"error": "Post not liked"}, status=status.HTTP_400_BAD_REQUEST
            )
        like.delete()
        return Response(
            {"message": "Post unliked successfully"}, status=status.HTTP_204_NO_CONTENT
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
        permission_classes=[IsAuthenticated],
    )
    def create_comment(self, request, pk=None):
        """Create a comment for a specific post"""
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["GET"], permission_classes=[IsAuthenticated])
    def comments(self, request, pk=None):
        """Retrieve all comments for a specific post"""
        post = self.get_object()
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticated]

# def perform_create(self, serializer):
#     serializer.save(author=self.request.user)
#
# @action(detail=True, methods=["GET"], permission_classes=[IsAuthenticated])
# def comments(self, request, pk=None):
#     """Retrieve all comments for a specific post"""
#     post = self.get_object()
#     comments = Comment.objects.filter(post=post)
#     serializer = self.get_serializer(comments, many=True)
#     return Response(serializer.data)
#
# @action(
#     detail=True,
#     methods=["POST"],
#     url_path="post/(?P<post_id>[^/.]+)/comments",
#     permission_classes=[IsAuthenticated],
# )
# def create_comment(self, request, post_id=None):
#     """Create a comment for a specific post"""
#     post = Post.objects.get(pk=post_id)
#     serializer = self.get_serializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save(author=self.request.user, post=post)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
