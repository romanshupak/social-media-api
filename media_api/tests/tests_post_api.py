from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

from media_api.models import Post, Like, Comment
from media_api.serializers import PostSerializer

POSTS_URL = reverse("media_api:post-list")


def detail_url(post_id):
    """Create and return URL for detail post view"""
    return reverse("media_api:post-detail", args=[post_id])


def sample_user(**params):
    """Create and return a sample user."""
    return get_user_model().objects.create_user(**params)


def sample_post(author, **params):
    """Create and return a sample post."""
    defaults = {
        "content": "Sample post content",
    }
    defaults.update(params)
    return Post.objects.create(author=author, **defaults)


def comment_detail_url(comment_id):
    """Create and return URL for detail comment view"""
    return reverse("media_api:comment-detail", args=[comment_id])


def sample_comment(author, post, **params):
    """Create and return a sample comment."""
    defaults = {
        "content": "Sample comment content",
    }
    defaults.update(params)
    return Comment.objects.create(author=author, post=post, **defaults)


class PublicPostApiTests(TestCase):
    """Test the public features of the post API."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required to access the posts."""
        res = self.client.get(POSTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePostApiTests(TestCase):
    """Test the authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = sample_user(email="testuser@example.com", password="testpass")
        self.client.force_authenticate(user=self.user)

    def test_retrieve_posts(self):
        """Test retrieving a list of posts."""
        sample_post(author=self.user)
        sample_post(author=self.user, content="Another sample post")

        res = self.client.get(POSTS_URL)

        posts = Post.objects.all().order_by("id")
        serializer = PostSerializer(posts, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(sorted(res.data, key=lambda x: x["id"]), serializer.data)

    def test_create_post(self):
        """Test creating a new post."""
        payload = {
            "content": "New post content",
        }
        res = self.client.post(POSTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        post = Post.objects.get(id=res.data["id"])
        self.assertEqual(post.content, payload["content"])

    def test_update_post(self):
        """Test updating a post."""
        post = sample_post(author=self.user)

        payload = {"content": "Updated post content"}
        url = detail_url(post.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.content, payload["content"])

    def test_delete_post(self):
        """Test deleting an existing post."""
        post = sample_post(author=self.user)
        url = detail_url(post.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=post.id).exists())

    def test_like_post(self):
        """Test liking a post."""
        post = sample_post(author=self.user)
        url = reverse("media_api:post-like", args=[post.id])
        res = self.client.post(url)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(post=post, user=self.user).exists())

    def test_dislike_post(self):
        """Test disliking a post."""
        post = sample_post(author=self.user)
        Like.objects.create(post=post, user=self.user)
        url = reverse("media_api:post-unlike", args=[post.id])
        res = self.client.post(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Like.objects.filter(post=post, user=self.user).exists())

    def test_add_comment_to_post(self):
        """Test adding a comment to a post."""
        post = sample_post(author=self.user)
        url = reverse("media_api:post-add-comment", args=[post.id])
        payload = {
            "content": "Test comment",
            "post": post.id,
        }

        res = self.client.post(url, payload)

        # Debugging output
        print(res.data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Comment.objects.filter(post=post, content=payload["content"]).exists()
        )

    def test_view_comments(self):
        """Test viewing comments to the post."""
        post = sample_post(author=self.user)
        Comment.objects.create(post=post, author=self.user, content="Test comment")
        url = reverse("media_api:post-comments", args=[post.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_update_comment(self):
        """Test updating a comment."""
        post = sample_post(author=self.user)
        comment = sample_comment(author=self.user, post=post)

        payload = {"content": "Updated comment"}
        url = comment_detail_url(comment.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()
        self.assertEqual(comment.content, payload["content"])

    def test_delete_comment(self):
        """Test deleting a comment."""
        post = sample_post(author=self.user)
        comment = sample_comment(author=self.user, post=post)

        url = comment_detail_url(comment.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())
