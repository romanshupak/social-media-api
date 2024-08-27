from celery import shared_task
from django.utils import timezone
from media_api.models import Post
from django.contrib.auth import get_user_model


@shared_task
def create_scheduled_post(content, user_id, scheduled_time):
    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
        # Перевірка, чи настав час для створення посту
        if timezone.now() >= scheduled_time:
            Post.objects.create(author=user, content=content)
            return "Post created successfully"
        else:
            return "Scheduled time not reached yet"
    except User.DoesNotExist:
        return "User not found"
