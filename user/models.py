from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser

from franchise.models import Franchise


class CustomUser(AbstractUser):
    # Add any additional fields here if needed
    # For example: phone_number = models.CharField(max_length=20, blank=True)
    # No need to define username, email, or password, as they are already in AbstractUser
    franchise = models.ForeignKey(Franchise, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('franchise', 'Franchise'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES,default='franchise')



def __str__(self):
    return self.email
