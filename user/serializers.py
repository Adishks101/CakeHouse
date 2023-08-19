# user/serializers.py
from datetime import datetime

from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'date_joined', 'phone_number',
                  'user_type', 'created_at', 'updated_at']  # Include other fields if needed
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'email': {'required': True},  # Make sure the email is provided

        }

    def create(self, validated_data):
        # Set the username the same as the email
        username = validated_data['email'].strip()
        name = validated_data['first_name'].strip() + " " + validated_data['last_name'].strip()
        validated_data['username'] = username
        # Create the user
        user = CustomUser.objects.create_user(
            username=username,
            email=validated_data['email'],
            name=name,
            first_name=validated_data['first_name'].strip(),
            last_name=validated_data['last_name'].strip(),
            password=validated_data['password'].strip(),
            phone_number=validated_data['phone_number'].strip(),
            is_superuser=True,
            date_joined=validated_data['date_joined'],
            is_staff=True,
            user_type=validated_data['user_type']

            # Include other fields if needed
        )
        return user

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_phone_number(self, value):
        if CustomUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already exists")
        return value


# user/serializers.py


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['admin'] = user.user_type == 'admin'
        return token


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)
