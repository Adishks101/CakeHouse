from Bakery_Management_System.custom_mixin_response import CustomResponseMixin
from rest_framework import generics
from rest_framework.generics import UpdateAPIView
from user.permissions import IsAdminUser, IsUser
from .models import Inventory
from .serializers import InventorySerializer, UpdateInventoryQuantitySerializer, RetrieveInventorySerializer


class InventoryCreateView(CustomResponseMixin, generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class InventoryListView(CustomResponseMixin, generics.ListAPIView):
    permission_classes = [IsUser]
    serializer_class = RetrieveInventorySerializer

    def get_queryset(self):
        user_type = self.request.user.user_type
        if user_type == 'admin':
            # Return the queryset for admin users
            return Inventory.objects.all()
        elif user_type == 'franchise':
            # Return the queryset for franchise users
            return Inventory.objects.filter(franchise=self.request.user.franchise)
        else:
            # Return an empty queryset or raise an error based on your requirement
            return Inventory.objects.none()

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return Inventory.objects.all()
        elif user.user_type == 'franchise':
            return Inventory.objects.filter(franchise=user.franchise)


class InventoryListViewByFranchise(CustomResponseMixin, generics.ListAPIView):
    permission_classes = [IsUser]
    serializer_class = RetrieveInventorySerializer

    def get_queryset(self):
        user_type = self.request.user.user_type
        franchise_id = self.kwargs['franchise']
        if user_type == 'admin':
            # Return the queryset for admin users
            return Inventory.objects.all()
        elif user_type == 'franchise':
            # Return the queryset for franchise users
            return Inventory.objects.filter(franchise=self.request.user.franchise)
        else:
            return Inventory.objects.none()


class InventoryDetailView(CustomResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsUser]
    serializer_class = RetrieveInventorySerializer

    def get_queryset(self):
        user_type = self.request.user.user_type
        if user_type == 'admin':
            # Return the queryset for admin users
            return Inventory.objects.all()
        elif user_type == 'franchise':
            # Return the queryset for franchise users
            return Inventory.objects.filter(franchise=self.request.user.franchise)
        else:
            # Return an empty queryset or raise an error based on your requirement
            return Inventory.objects.none()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UpdateInventoryQuantityView(CustomResponseMixin, UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Inventory.objects.all()
    serializer_class = UpdateInventoryQuantitySerializer

    def perform_update(self, serializer):
        inventory_item = self.get_object()
        new_quantity = serializer.validated_data['quantity']
        inventory_item.available_quantity = new_quantity
        inventory_item.save()
