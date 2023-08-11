from django.contrib.auth.hashers import make_password
from django.db import models
import re
from django import forms


class Franchise(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, blank=True)
    password = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    username = models.EmailField()
    contact_email = models.EmailField()
    pin = models.CharField(max_length=6)
    phone_number = models.CharField(max_length=20)
    date_established = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean_pin(self):
        pin = self.cleaned_data.get('pin')
        if pin:
            # Use a regular expression to check if the PIN contains only 6 digits
            if not re.match(r'^\d{6}$', pin):
                raise forms.ValidationError("Invalid PIN. It must be a 6-digit number.")

            # Return the cleaned PIN
            return pin

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
    def save(self, *args, **kwargs):
        # Hash the password before saving to the database
        if self.password:
            self.password = make_password(self.password)
        super(Franchise, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
# Create your models here.
