# serializers.py
from rest_framework import serializers
from franchise.serializers import FranchiseSerializer
from product.serializers import ProductSerializer
from .models import Inventory


class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory
        fields = ('id', 'franchise', 'product', 'available_quantity', 'total_sold', 'created_at', 'updated_at')
        extra_kwargs = {

            'total_sold': {'read_only': True}
        }


class UpdateInventoryQuantitySerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=0)


class RetrieveInventorySerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    franchise = FranchiseSerializer()
    class Meta:
        model = Inventory
        fields = '__all__'
