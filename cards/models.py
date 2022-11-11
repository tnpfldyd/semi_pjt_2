from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings

# Create your tests here.
class Card(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    is_private = models.BooleanField()
    is_indiv = models.BooleanField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="card"
    )
    socks = models.IntegerField()
    chimneys = models.IntegerField()


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="card_comment",
    )
    ribbons = models.IntegerField()
