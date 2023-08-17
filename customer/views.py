from Bakery_Management_System.custom_mixin_response import CustomResponseMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from user.permissions import IsUser
from .models import Customer
from .serializers import CustomerSerializer
from .filters import CustomerFilter


class CustomerListCreateView(CustomResponseMixin, generics.ListCreateAPIView):
    permission_classes = [IsUser]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomerFilter


class CustomerRetrieveUpdateDestroyView(CustomResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsUser]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
