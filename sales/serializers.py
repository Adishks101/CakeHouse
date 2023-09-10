# serializers.py
from customer.models import Customer
from rest_framework import serializers

from customer.serializers import CustomerSerializer
from franchise.serializers import FranchiseSerializer
from product.models import Product
from product.serializers import ProductSerializer
from user.serializers import CustomUserSerializer
from .models import Sales, SaleItem


class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = '__all__'


class SalesSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, read_only=True)
    user = CustomUserSerializer()
    customer = CustomerSerializer()
    franchise = FranchiseSerializer()

    class Meta:
        model = Sales
        fields = ('id', 'items', 'customer', 'user', 'franchise', 'payment_mode',
                  'total_amount',
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
    items = SaleItemSerializer(many=True, read_only=True)
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255, required=False)
    phone_number = serializers.CharField(max_length=20, required=True)
    payment_mode = serializers.ChoiceField(choices=PAYMENT_MODE_CHOICES, required=True)
    total_amount = serializers.IntegerField(required=True)
    extra_kwargs = {

        'id': {'read_only': True}
    }

    def create(self, validated_data):
        name = validated_data.pop('name')
        phone_number = validated_data.pop('phone_number')

        # Check if a customer with the given phone number already exists
        try:
            customer = Customer.objects.get(phone_number=phone_number)
        except Customer.DoesNotExist:
            # Customer does not exist, create a new one
            customer = Customer.objects.create(name=name, phone_number=phone_number)
        customer.update_points(validated_data['total_amount'])
        validated_data['user'] = self.context['request'].user
        validated_data['customer'] = customer

        try:
            items_data = validated_data.pop('items')
            sale = Sales.objects.create(**validated_data)
            for item_data in items_data:
                SaleItem.objects.create(sales=sale, **item_data)
            return sale
        except Exception as e:
            error_msg = "Failed to create sale."
            return {"error_msg": error_msg, "exception": str(e)}
