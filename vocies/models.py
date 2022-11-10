from django.db import models
from django.conf import settings

# Create your models here.


class Vocie(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="vocie/", blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="vocies"
    )


class Comment(models.Model):
    content = models.TextField()
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vocie = models.ForeignKey(Vocie, on_delete=models.CASCADE, related_name="vocie_comment")
    created_at = models.DateTimeField(auto_now_add=True)
