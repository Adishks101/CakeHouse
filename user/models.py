from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # Add any additional fields here if needed
    # For example: phone_number = models.CharField(max_length=20, blank=True)
    # No need to define username, email, or password, as they are already in AbstractUser
    phone_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def __str__(self):
    return self.email
