from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):

    # Additional fields
    phone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=50, default = "guest")

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['role', 'email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username
