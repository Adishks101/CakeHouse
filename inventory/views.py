from rest_framework import generics
from rest_framework.generics import UpdateAPIView
from rest_framework.mixins import ListModelMixin, UpdateModelMixin

from user.permissions import IsAdminUser
from .models import Inventory
from .serializers import InventorySerializer, UpdateInventoryQuantitySerializer


class InventoryCreateView(generics.CreateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class InventoryListView(generics.ListAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return Inventory.objects.all()
        elif user.user_type == 'franchise':
            return Inventory.objects.filter(franchise=user.franchise)



class InventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def get_queryset(self):
        return self.queryset.filter(franchise=self.request.user.franchise)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UpdateInventoryQuantityView(UpdateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = UpdateInventoryQuantitySerializer
    permission_classes = [IsAdminUser]

    def perform_update(self, serializer):
        inventory_item = self.get_object()
        new_quantity = serializer.validated_data['quantity']
        inventory_item.available_quantity = new_quantity
        inventory_item.save()
