# user/serializers.py
from datetime import datetime

from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'date_joined', 'phone_number', 'user_type', 'created_at', 'updated_at']  # Include other fields if needed
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': False, 'read_only': True},  # Allow the username to be optional
            'email': {'required': True},  # Make sure the email is provided


        }

    def create(self, validated_data):
        # Set the username the same as the email
        username = validated_data.get('username') or validated_data['email']
        validated_data['username'] = username
        # Create the user
        user = CustomUser.objects.create_user(
            username=username,
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            phone_number=validated_data['phone_number'],
            is_superuser=True,
            date_joined=validated_data['date_joined'],
            is_staff=True,

            # Include other fields if needed
        )
        return user


# user/serializers.py


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Customize the token payload here (if needed)
        # For example, you can add custom user fields to the token
        token['admin'] = user.is_superuser

        return token
