# serializers.py
from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

        extra_kwargs = {
            'email': {'required': True},  # Make sure the email is provided
            'points': {'read_only': True}

        }