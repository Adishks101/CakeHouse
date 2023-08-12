# views.py
from django.contrib.auth import get_user_model
from rest_framework import generics

from user.permissions import IsAdminUser
from .models import Franchise
from .serializers import FranchiseSerializer, FranchiseUpdateSerializer

CustomUser = get_user_model()


class FranchiseListView(generics.ListAPIView):
    queryset = Franchise.objects.all()
    serializer_class = FranchiseSerializer


class FranchiseCreateView(generics.CreateAPIView):
    # permission_classes = [IsAdminUser]

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


class FranchiseDetailView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAdminUser]
    queryset = Franchise.objects.all()
    serializer_class = FranchiseUpdateSerializer
