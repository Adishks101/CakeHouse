# serializers.py
from rest_framework import serializers

from user.models import CustomUser
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
            franchise = Franchise.objects.get(phone_number=value)

            raise serializers.ValidationError({"message": "Phone number already registered"})
        except Franchise.DoesNotExist:
            try:
                user = CustomUser.objects.get(phone_number=value)
                raise serializers.ValidationError({"message": "Phone number already registered as user."})
            except CustomUser.DoesNotExist:
                return value

    def validate_email(self, value):
        try:
            # Check if a Franchise with the given email already exists
            customer = Franchise.objects.get(email=value)
            raise serializers.ValidationError({"message": "Email id already registered"})
        except Franchise.DoesNotExist:
            try:
                user = CustomUser.objects.get(email=value)
                raise serializers.ValidationError({"message": "Email already registered as user."})
            except CustomUser.DoesNotExist:
                return value

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {'status': 1, 'message': 'Franchise created successfully', 'data': data}


class FranchiseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Franchise
        exclude = ['password']

        extra_kwargs = {
            'email': {'read_only': True},
            'username': {'read_only': True}

        }
