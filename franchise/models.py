from django.db import models


class Franchise(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, blank=True)
    password = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    username = models.EmailField()
    contact_email = models.EmailField()
    pin = models.IntegerField(max_length=6)
    phone_number = models.CharField(max_length=20)
    date_established = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Add other fields specific to the Franchise model

    def __str__(self):
        return self.name
# Create your models here.
