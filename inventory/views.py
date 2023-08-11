from rest_framework import generics
from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from .models import Inventory
from .serializers import InventorySerializer


class InventoryListView(ListModelMixin, generics.GenericAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def get_queryset(self):
        return self.queryset.filter(franchise=self.request.user.franchise)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class InventoryDetailView(UpdateModelMixin, generics.RetrieveAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def get_queryset(self):
        return self.queryset.filter(franchise=self.request.user.franchise)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
