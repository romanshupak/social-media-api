from rest_framework import filters

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
    search_fields = [
        "content",
    ]

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


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
