from Bakery_Management_System.custom_mixin_response import CustomResponseMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, filters
from inventory.models import Inventory
from user.permissions import IsAdminUser, IsFranchiseOwner, IsFranchiseUser, IsUser
from . import serializers
from .filteras import SalesFilter
from .models import Sales
from .serializers import SalesCreateSerializer, SalesSerializer


class SalesListView(CustomResponseMixin, generics.ListAPIView):
    permission_classes = [IsFranchiseOwner]
    serializer_class = SalesSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = SalesFilter
    search_fields = ['total_amount', 'quantity_sold']
    ordering_fields = ['price', 'created_at']

    def get_queryset(self):
        user_type = self.request.user.user_type
        if user_type == 'admin':
            # Return the queryset for admin users
            return Sales.objects.all()
        elif user_type == 'franchise':
            # Return the queryset for franchise users
            return Sales.objects.filter(franchise=self.request.user.franchise)
        else:
            # Return an empty queryset or raise an error based on your requirement
            return Inventory.objects.none()


class SalesDetailView(CustomResponseMixin, generics.RetrieveAPIView):
    permission_classes = [IsUser]
    serializer_class = SalesSerializer

    def get_queryset(self):
        user_type = self.request.user.user_type
        franchise_id = self.kwargs['franchise']
        if user_type == 'admin':
            # Return the queryset for admin users
            return Sales.objects.filter(id=franchise_id)
        elif user_type == 'franchise':
            # Return the queryset for franchise users
            return Sales.objects.filter(franchise=self.request.user.franchise, id=franchise_id)
        else:
            # Return an empty queryset or raise an error based on your requirement
            return Inventory.objects.none()


class SaleCreateView(CustomResponseMixin, generics.CreateAPIView):
    permission_classes = [IsFranchiseUser]
    queryset = Sales.objects.all()
    serializer_class = SalesCreateSerializer

    def perform_create(self, serializer):
        inventory = Inventory.objects.get(product=serializer.validated_data['product'],
                                          franchise=self.request.user.franchise)
        if inventory.available_quantity < serializer.validated_data['quantity_sold']:
            raise serializers.ValidationError("Insufficient inventory.")
        serializer.save(franchise=self.request.user.franchise)
        inventory.update_available_quantity(serializer.validated_data['quantity_sold'])
