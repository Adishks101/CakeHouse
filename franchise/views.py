# views.py
from django.contrib.auth import get_user_model
from Bakery_Management_System.custom_mixin_response import CustomResponseMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from user.permissions import IsAdminUser, IsFranchiseOwner, IsUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import FranchiseFilter
from .models import Franchise
from .serializers import FranchiseSerializer, FranchiseUpdateSerializer

CustomUser = get_user_model()


class FranchiseListView(CustomResponseMixin, generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Franchise.objects.all()
    serializer_class = FranchiseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = FranchiseFilter
    search_fields = ['name', 'location']
    ordering_fields = ['name']


class FranchiseCreateView(CustomResponseMixin, generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = FranchiseSerializer

    def perform_create(self, serializer):
        franchise = serializer.save()

        # Create a user associated with the franchise
        user = CustomUser.objects.create(
            email=franchise.username,
            username=franchise.username,
            franchise=franchise,
            user_type='franchise',
            phone_number=franchise.phone_number,
            password=franchise.password
        )
        user.save()


class FranchiseDetailView(CustomResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsUser]
    serializer_class = FranchiseUpdateSerializer

    def get_queryset(self):
        user_type = self.request.user.user_type
        franchise_id = self.kwargs['franchise']
        if user_type == 'admin':
            # Return the queryset for admin users
            return Franchise.objects.all()
        elif user_type == 'franchise':
            # Return the queryset for franchise users
            return Franchise.objects.get(id=self.request.user.franchise)
        else:
            # Return an empty queryset or raise an error based on your requirement
            return Franchise.objects.none()
