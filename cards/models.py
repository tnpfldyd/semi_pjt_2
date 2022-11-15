from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings

# Create your tests here.
class UserCard(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    socks = models.IntegerField(blank=True)
    chimneys = models.IntegerField(blank=True)


class Groupcard(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    is_private = models.BooleanField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    socks = models.IntegerField()
    chimneys = models.IntegerField()


class UserComment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    usercard = models.ForeignKey(UserCard, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    ribbons = models.IntegerField()
    id_text = models.TextField(blank=True)


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    usercard = models.ForeignKey(UserCard, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="card_comment",
    )
    ribbons = models.IntegerField()
    id_text = models.TextField(blank=True)


class Groupcomment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    groupcard = models.ForeignKey(Groupcard, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="groupcard_comment",
    )
    ribbons = models.IntegerField()
    id_text = models.TextField(blank=True)
