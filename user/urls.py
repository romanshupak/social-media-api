from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.views import (
    CreateUserView,
    ManageUserView,
    LogoutView,
    UserSearchView,
    FollowUnfollowView,
    ListFollowingView,
    ListFollowersView,
)

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/<int:id>/", ManageUserView.as_view(), name="user-profile"),
    path("search/", UserSearchView.as_view(), name="user-search"),
    path("<int:pk>/follow/", FollowUnfollowView.as_view(), name="follow-user"),
    path(
        "<int:pk>/unfollow/",
        FollowUnfollowView.as_view(),
        name="unfollow-user"
    ),
    path("me/following/", ListFollowingView.as_view(), name="list-following"),
    path("me/followers/", ListFollowersView.as_view(), name="list-followers"),
]
