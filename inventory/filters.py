import django_filters
from .models import Inventory


class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Inventory
        fields = {
           
        }
