from django.test import TestCase

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from rest_framework.reverse import reverse

USER_URL = reverse("user:create")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class UserSerializerTests(TestCase):
    """Test UserSerializer functionality"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        """Test creating a user"""
        payload = {
            "email": "testuser@example.com",
            "password": "testpass123",
            "is_staff": False,
        }
        res = self.client.post(USER_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertEqual(user.email, payload["email"])
        self.assertFalse(user.is_staff)

    def test_create_user_with_no_password(self):
        """Test creating a user with no password"""
        payload = {
            "email": "testuser@example.com",
        }
        res = self.client.post(USER_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", res.data)

    def test_retrieve_user_profile(self):
        """Test retrieving user profile"""
        user = create_user(email="testuser@example.com", password="testpass123")
        self.client.force_authenticate(user=user)

        res = self.client.get(reverse("user:manage"))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["email"], user.email)

    def test_update_user_profile(self):
        """Test updating the user profile"""
        user = create_user(email="testuser@example.com", password="testpass123")
        self.client.force_authenticate(user=user)

        payload = {"bio": "Updated bio"}
        res = self.client.patch(reverse("user:manage"), payload)

        user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(user.bio, payload["bio"])

    def test_delete_user_profile(self):
        """Test deleting the user profile"""
        user = create_user(email="testuser@example.com", password="testpass123")
        self.client.force_authenticate(user=user)

        res = self.client.delete("/api/user/me/")

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(get_user_model().objects.filter(email=user.email).exists())

    def test_follow_user(self):
        """Test following another user"""
        user = create_user(email="user1@example.com", password="testpass123")
        target_user = create_user(email="user2@example.com", password="testpass123")
        self.client.force_authenticate(user=user)

        res = self.client.post(
            reverse("user:follow-user", args=[target_user.id]), {"action": "follow"}
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(target_user, user.following.all())

    def test_unfollow_user(self):
        """Test unfollowing another user"""
        user = create_user(email="user1@example.com", password="testpass123")
        target_user = create_user(email="user2@example.com", password="testpass123")
        user.following.add(target_user)
        self.client.force_authenticate(user=user)

        res = self.client.post(
            reverse("user:unfollow-user", args=[target_user.id]), {"action": "unfollow"}
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn(target_user, user.following.all())

    def test_search_users(self):
        """Test searching for users"""
        create_user(email="user1@example.com", password="testpass123", bio="bio 1")
        create_user(email="user2@example.com", password="testpass123", bio="bio 2")

        self.client.force_authenticate(
            user=create_user(email="user3@example.com", password="testpass123")
        )

        res = self.client.get(reverse("user:user-search"), {"search": "bio"})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
