from rest_framework import generics, status
from rest_framework.response import Response
from inventory.models import Inventory
from . import serializers
from .models import Sales
from .serializers import SalesSerializer


class SalesListView(generics.ListAPIView):
    serializer_class = SalesSerializer

    def get_queryset(self):
        return Sales.objects.filter(franchise=self.request.user.franchise)


class SalesDetailView(generics.RetrieveAPIView):
    serializer_class = SalesSerializer

    def get_queryset(self):
        return Sales.objects.filter(franchise=self.request.user.franchise)


class SaleCreateView(generics.CreateAPIView):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer

    def perform_create(self, serializer):
        # Retrieve the inventory object
        inventory = Inventory.objects.get(product=serializer.validated_data['product'],
                                          franchise=self.request.user.franchise)
        if inventory.available_quantity < serializer.validated_data['quantity_sold']:
            raise serializers.ValidationError("Insufficient inventory.")
        sale = serializer.save(franchise=self.request.user.franchise)
        inventory.update_available_quantity(serializer.validated_data['quantity_sold'])
