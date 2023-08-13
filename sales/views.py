from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, filters
from rest_framework.response import Response
from inventory.models import Inventory
from . import serializers
from .filteras import SalesFilter
from .models import Sales
from .serializers import SalesSerializer


class SalesListView(generics.ListAPIView):
    serializer_class = SalesSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = SalesFilter
    search_fields = ['total_amount', 'quantity_sold']
    ordering_fields = ['price', 'created_at']

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
        inventory = Inventory.objects.get(product=serializer.validated_data['product'],
                                          franchise=self.request.user.franchise)
        if inventory.available_quantity < serializer.validated_data['quantity_sold']:
            raise serializers.ValidationError("Insufficient inventory.")
        serializer.save(franchise=self.request.user.franchise)
        inventory.update_available_quantity(serializer.validated_data['quantity_sold'])
