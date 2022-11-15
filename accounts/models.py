from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.


class User(AbstractUser):
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )
    blocking = models.ManyToManyField(
        "self", symmetrical=False, related_name="blockers"
    )
    updated_at = models.DateTimeField(auto_now=True)
    profileimage = models.ImageField(upload_to="profile/", blank=True)
    gender = models.CharField(blank=True, max_length=10)
    age_range = models.CharField(blank=True, max_length=10)
    nickname = models.CharField(max_length=40, blank=True)
    introduce = models.CharField(blank=True, max_length=200)
    refresh_token = models.TextField(blank=True)
