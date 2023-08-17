# views.py
from Bakery_Management_System.custom_mixin_response import CustomResponseMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from user.permissions import IsAdminUser, IsUser

from .filters import ProductFilter
from .models import Product
from .serializers import ProductSerializer


class ProductListAPIView(CustomResponseMixin, generics.ListAPIView):
    permission_classes = [IsUser]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'price', 'quantity']
    ordering_fields = ['price']

class ProductCreateAPIView(CustomResponseMixin, generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(CustomResponseMixin,generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsUser]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'price', 'quantity']
    ordering_fields = ['price']
