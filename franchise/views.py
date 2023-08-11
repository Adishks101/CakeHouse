# views.py
from rest_framework import generics
from .models import Franchise
from .serializers import FranchiseSerializer

class FranchiseListView(generics.ListCreateAPIView):
    queryset = Franchise.objects.all()
    serializer_class = FranchiseSerializer

class FranchiseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Franchise.objects.all()
    serializer_class = FranchiseSerializer
