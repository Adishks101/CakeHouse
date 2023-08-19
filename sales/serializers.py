# serializers.py
from customer.models import Customer
from rest_framework import serializers

from customer.serializers import CustomerSerializer
from product.models import Product
from product.serializers import ProductSerializer
from user.serializers import CustomUserSerializer
from .models import Sales


class SalesSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    user = CustomUserSerializer()
    customer = CustomerSerializer()

    class Meta:
        model = Sales
        fields = (
            'product', 'customer', 'user', 'quantity_sold', 'quantity_type', 'payment_mode', 'total_amount',
            'sale_date', 'created_at',
            'updated_at')

    def create(self, validated_data):
        # Set the franchise (user) based on the authenticated user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class SalesCreateSerializer(serializers.Serializer):
    PAYMENT_MODE_CHOICES = (
        ('cash', 'Cash'),
        ('bank', 'Bank'),
    )
    QUANTITY_TYPE_CHOICES = (
        ('cash', 'Cash'),
        ('bank', 'Bank'),
    )
    name = serializers.CharField(max_length=255, required=False)
    phone_no = serializers.CharField(max_length=20, required=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=True)
    quantity_sold = serializers.IntegerField(required=True)
    quantity_type = serializers.ChoiceField(choices=QUANTITY_TYPE_CHOICES, required=True)
    payment_mode = serializers.ChoiceField(choices=PAYMENT_MODE_CHOICES, required=True)
    total_amount = serializers.IntegerField(required=True)

    def create(self, validated_data):
        name = validated_data.pop('name')
        phone_number = validated_data.pop('phone_number')

        # Check if a customer with the given phone number already exists
        try:
            customer = Customer.objects.get(phone_number=phone_number)
        except Customer.DoesNotExist:
            # Customer does not exist, create a new one
            customer = Customer.objects.create(name=name, phone_number=phone_number)

        validated_data['user'] = self.context['request'].user
        validated_data['customer'] = customer

        sales = Sales.objects.create(**validated_data)

        return sales
