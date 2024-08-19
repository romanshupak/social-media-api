from django.urls import path, include
from rest_framework import routers

from media_api.views import PostViewSet, CommentViewSet, LikeViewSet

router = routers.DefaultRouter()
router.register("posts", PostViewSet)
router.register("comments", CommentViewSet)
router.register("likes", LikeViewSet)


urlpatterns = [path("", include(router.urls))]

app_name = "media_api"
