from django.urls import path, include
from rest_framework import routers

from media_api.views import PostViewSet, LikeViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register("posts", PostViewSet)
router.register("comments", CommentViewSet)
router.register("likes", LikeViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path(
        "posts/<int:post_id>/add-comment/",
        PostViewSet.as_view({"post": "create_comment"}),
        name="post-add-comment",
    ),
]

app_name = "media_api"
