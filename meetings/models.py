from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings

# Create your models here.


class Meeting(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    image = ProcessedImageField(
        upload_to="images/",
        blank=True,
        processors=[ResizeToFill(700, 700)],
        format="JPEG",
        options={"quality": 90},
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="meeting"
    )

    is_closed = models.BooleanField(default=True)
    password = models.CharField(max_length=4, blank=True, null=True)
    location_choices = [
        ("강남구", "강남구" ), 
        ("광진구", "광진구"),
        ("노원구", "노원구"),
        ("동작구", "동작구"),
        ("마포구", "마포구"),
        ("성동구", "성동구"),
        ("송파구", "송파구"),
        ("서초구", "서초구"),
        ("용산구", "용산구"),
        ("영등포구", "영등포구"),
        ("용산구", "용산구"),
    ]
    location = models.CharField(
        max_length=20,
        choices=location_choices,
        default="선택",
    )
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    belong = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="belongs", blank=True)
    # enter_record = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="enter_records", blank=True)


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="meeting_comment"
    )
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
