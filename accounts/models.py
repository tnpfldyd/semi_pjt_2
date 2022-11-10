from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.


class User(AbstractUser):
    followings = models.ManyToManyField("self", symmetrical=False, related_name="followers")
    blocking = models.ManyToManyField("self", symmetrical=False, related_name="blockers")
    secession = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    kakao_id = models.BigIntegerField(blank=True, unique=True)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    introduce = models.TextField(blank=True)
    nickname = models.CharField(max_length=40, blank=True)
    gender = models.BooleanField(blank=True)
    age = models.DateField(blank=True)
    profileimage = models.ImageField(upload_to="profile/", blank=True)
