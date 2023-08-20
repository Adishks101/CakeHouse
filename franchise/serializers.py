# serializers.py
from rest_framework import serializers
from .models import Franchise


class FranchiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Franchise
        fields = '__all__'

        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},  # Make sure the email is provided
            'is_active': {'read_only': True}

        }

    def validate_phone_number(self, value):
        try:
            # Check if a Franchise with the given phone number already exists
            customer = Franchise.objects.get(phone_number=value)
            raise serializers.ValidationError({"message": "Phone number already registered"})
        except Franchise.DoesNotExist:
            return value

    def validate_email(self, value):
        try:
            # Check if a Franchise with the given email already exists
            customer = Franchise.objects.get(email=value)
            raise serializers.ValidationError({"message": "Email id already registered"})
        except Franchise.DoesNotExist:
            return value


class FranchiseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Franchise
        exclude = ['password']

        extra_kwargs = {
            'email': {'read_only': True},
            'is_active': {'read_only': True},
            'username': {'read_only': True}

        }
