from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.


class User(AbstractUser):
    followings = models.ManyToManyField("self", symmetrical=False, related_name="followers")
    blocking = models.ManyToManyField("self", symmetrical=False, related_name="blockers")
    secession = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    profileimage = models.ImageField(upload_to="profile/", blank=True)
    gender = models.TextField(blank=True)
    age_range = models.TextField(blank=True)
    nickname = models.CharField(max_length=40, blank=True)
    introduce = models.TextField(blank=True)
