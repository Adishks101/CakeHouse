# serializers.py
from rest_framework import serializers
from .models import Inventory


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('franchise', 'product', 'available_quantity', 'total_sold', 'created_at', 'updated_at')
        extra_kwargs = {

            'total_sold': {'read_only': True}
        }


class UpdateInventoryQuantitySerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=0)
