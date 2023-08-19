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

    def validate_phone_number(self, value):
        if Customer.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already exists")
        return value
