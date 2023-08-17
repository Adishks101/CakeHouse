from Bakery_Management_System.custom_mixin_response import CustomResponseMixin
from rest_framework import generics
from rest_framework.generics import UpdateAPIView
from rest_framework.mixins import ListModelMixin, UpdateModelMixin

from user.permissions import IsAdminUser, IsFranchiseOwner
from .models import Inventory
from .serializers import InventorySerializer, UpdateInventoryQuantitySerializer, RetrieveInventorySerializer


class InventoryCreateView(CustomResponseMixin,generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class InventoryListView(CustomResponseMixin,generics.ListAPIView):
    permission_classes = [IsFranchiseOwner,IsAdminUser]
    queryset = Inventory.objects.all()
    serializer_class = RetrieveInventorySerializer

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return Inventory.objects.all()
        elif user.user_type == 'franchise':
            return Inventory.objects.filter(franchise=user.franchise)


class InventoryListViewByFranchise(CustomResponseMixin,generics.ListAPIView):
    permission_classes = [IsFranchiseOwner,IsAdminUser]
    serializer_class = RetrieveInventorySerializer

    def get_queryset(self):
        franchise_id = self.kwargs['franchise']  # Retrieve the franchise_id path variable
        return Inventory.objects.filter(franchise=franchise_id)


class InventoryDetailView(CustomResponseMixin,generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsFranchiseOwner,IsAdminUser]
    queryset = Inventory.objects.all()
    serializer_class = RetrieveInventorySerializer

    def get_queryset(self):
        return self.queryset.filter(franchise=self.request.user.franchise)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UpdateInventoryQuantityView(CustomResponseMixin,UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Inventory.objects.all()
    serializer_class = UpdateInventoryQuantitySerializer
    permission_classes = [IsAdminUser]

    def perform_update(self, serializer):
        inventory_item = self.get_object()
        new_quantity = serializer.validated_data['quantity']
        inventory_item.available_quantity = new_quantity
        inventory_item.save()
