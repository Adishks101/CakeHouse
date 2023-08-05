# user/serializers.py

from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','first_name','last_name','email','password','date_joined','phone_number','is_superuser','is_staff','created_at','updated_at']  # Include other fields if needed
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': False,'read_only':True},  # Allow the username to be optional
            'email': {'required': True},     # Make sure the email is provided
            'created_at':{'read_only':True},
            'updated_at':{'read_only':True},

        }

    def create(self, validated_data):
        # Set the username the same as the email
        username = validated_data.get('username') or validated_data['email']
        validated_data['username'] = username

        # Create the user
        user = CustomUser.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data['phone_number'],
            is_superuser=validated_data['is_superuser'],
            date_joined=validated_data['date_joined'],
            is_staff=validated_data['is_staff']

            # Include other fields if needed
        )
        return user
