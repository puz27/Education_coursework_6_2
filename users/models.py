from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Model for user"""
    username = None

    email = models.EmailField(unique=True, verbose_name="user Email")
    phone = models.CharField(max_length=50, verbose_name="phone number", null=True, blank=True)
    country = models.CharField(max_length=50, verbose_name="user country", null=True, blank=True)
    avatar = models.ImageField(upload_to="images", null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
