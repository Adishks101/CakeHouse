from rest_framework.response import Response

from Bakery_Management_System.custom_mixin_response import CustomResponseMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, filters
from inventory.models import Inventory
from user.permissions import IsAdminUser, IsFranchiseOwner, IsFranchiseUser, IsUser
from . import serializers
from .filteras import SalesFilter
from .models import Sales
from .serializers import SalesCreateSerializer, SalesSerializer
from rest_framework import serializers


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
        try:
            inventory = Inventory.objects.get(product=serializer.validated_data['product'],
                                              franchise=self.request.user.franchise)
        except Inventory.DoesNotExist:
            raise serializers.ValidationError({"message":"Product not found in inventory."})
        if inventory.available_quantity < serializer.validated_data['quantity_sold']:
            raise serializers.ValidationError({"message": "Insufficient inventory."})
        sales = serializer.save(franchise=self.request.user.franchise)
        inventory.update_available_quantity(serializer.validated_data['quantity_sold'])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        sale_serializer = SalesSerializer(serializer.instance)
        return Response(data=sale_serializer.data, status=status.HTTP_201_CREATED)
