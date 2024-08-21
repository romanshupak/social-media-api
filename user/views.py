from django.contrib.auth import get_user_model
from rest_framework import generics, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers import UserSerializer, ImageUploadSerializer

User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def get_object(self):
        return self.request.user

    @action(
        methods=["POST"],
        detail=False,
        url_path="upload-image",
        permission_classes=[IsAuthenticated],
    )
    def upload_image(self, request, *args, **kwargs):
        """Endpoint for uploading user profile image"""
        serializer = ImageUploadSerializer(self.get_object(), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowUnfollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None):
        action = request.data.get("action")
        user = request.user
        try:
            target_user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if user == target_user:
            return Response(
                {"error": "Cannot follow/unfollow yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if action == "follow":
            user.following.add(target_user)
            return Response(
                {"message": "User followed successfully"}, status=status.HTTP_200_OK
            )
        elif action == "unfollow":
            user.following.remove(target_user)
            return Response(
                {"message": "User unfollowed successfully"}, status=status.HTTP_200_OK
            )
        return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)


class ListFollowingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        following_users = user.following.all()
        serializer = UserSerializer(following_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListFollowersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        followers_users = user.followers.all()
        serializer = UserSerializer(followers_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginUserView(APIView):
    def post(self, request):
        """Handle user login"""
        # Implementation for login can be here


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            token = RefreshToken(refresh_token)
            token.blacklist()  # Анулюємо токен, якщо ви використовуєте blacklist
            return Response(
                {"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserSearchView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["email", "bio"]  # Поля, за якими можна здійснювати пошук
