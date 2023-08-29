from django.db import models
import re
from django import forms


class Customer(models.Model):
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True, unique=True)
    phone_number = models.CharField(max_length=20, blank=False, unique=True)
    pin = models.CharField(max_length=6, blank=True)
    points = models.PositiveIntegerField(default=0)
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

    def update_points(self, points):
        self.points += points
        self.save()


    def __str__(self):
        return self.phone_number
