from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.viewsets import GenericViewSet

from media_api.models import Post, Comment, Like
from media_api.serializers import PostSerializer, CommentSerializer, LikeSerializer


class PostViewSet(GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class LikeViewSet(GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
