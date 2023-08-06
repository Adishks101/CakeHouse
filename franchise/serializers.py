# serializers.py
from rest_framework import serializers
from .models import Franchise


class FranchiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Franchise
        fields = ('id', 'name', 'created_at', 'updated_at')
