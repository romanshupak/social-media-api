from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=5)

    class Meta:
        model = get_user_model()
        fields = ("email", "bio", "avatar", "followers", "password")
        extra_kwargs = {
            "followers": {"required": False},
        }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        password = validated_data.pop("password", None)
        user = get_user_model().objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user
