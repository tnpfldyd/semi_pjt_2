from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

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
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_closed = models.BooleanField(default=True)
    password = models.CharField(max_length=4, blank=True, null=True)
    location_choices = [
      ('선택', None),
      ('노원구', '노원구'),
      ('송파구', '송파구'),
    ]
    location = models.CharField(
      max_length=20,
      choices = location_choices, 
      default='선택',
    )


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    meeting_id = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    