# Generated by Django 5.1 on 2024-08-22 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("media_api", "0002_post_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="hashtags",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
