# serializers.py
from rest_framework import serializers
from .models import Sales


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = ('product', 'user', 'quantity_sold', 'total_amount', 'sale_date', 'created_at', 'updated_at')
