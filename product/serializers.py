# serializers.py
from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'description', 'price', 'category', 'company', 'product_image', 'created_at',
            'updated_at')
        extra_kwargs = {
            'category': {'required': True},
            'name': {'required': True},
            'price': {'required': True},
            'product_image': {'required': False},
            'company': {'required': True},

        }
