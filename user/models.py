from django.db import models
from django.contrib.auth.models import AbstractUser
import re
from django.forms import forms
from franchise.models import Franchise


class CustomUser(AbstractUser):
    franchise = models.ForeignKey(Franchise, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('franchise', 'Franchise'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='franchise')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            # Remove any non-digit characters from the phone number
            cleaned_phone_number = re.sub(r'\D', '', phone_number)

            # Perform additional validation based on your requirements
            if len(cleaned_phone_number) < 10:
                raise forms.ValidationError("Invalid phone number. It must have at least 10 digits.")

            # Return the cleaned phone number
            return cleaned_phone_number


def __str__(self):
    return self.email
