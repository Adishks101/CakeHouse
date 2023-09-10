from rest_framework.response import Response

from Bakery_Management_System.custom_mixin_response import CustomResponseMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
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


class CustomerByPhoneNumberView(generics.RetrieveAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    lookup_field = 'phone_number'

    def get_object(self):
        # Get the customer object by phone number
        phone_number = self.kwargs.get('phone_number')
        try:
            return Customer.objects.get(phone_number=phone_number)
        except Customer.DoesNotExist:
            return None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({'error': 'Customer not found.'}, status=status.HTTP_404_NOT_FOUND)
