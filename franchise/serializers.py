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


class FranchiseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Franchise
        exclude = ['password']

        extra_kwargs = {
            'email': {'read_only': True},
            'is_active': {'read_only': True},
            'username': {'read_only': True}

        }
