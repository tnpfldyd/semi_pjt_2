from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    gender = models.BooleanField(blank=True)
    profileimg = models.ImageField(blank=True, upload_to="images/")
    introduce = models.CharField(max_length=100)
    age = models.DateField(blank=True)
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )
    blockings = models.ManyToManyField(
        "self", symmetrical=False, related_name="blockers"
    )
    pass
