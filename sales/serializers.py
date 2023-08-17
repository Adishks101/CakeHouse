# serializers.py
from rest_framework import serializers
from .models import Sales


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = (
            'product', 'quantity_sold', 'quantity_type', 'payment_mode', 'total_amount', 'sale_date', 'created_at',
            'updated_at')

    def create(self, validated_data):
        # Set the franchise (user) based on the authenticated user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
