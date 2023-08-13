import django_filters
from .models import Franchise


class FranchiseFilter(django_filters.FilterSet):
    class Meta:
        model = Franchise
        fields = {
            'name': ['exact', 'icontains'],
            'location': ['exact', 'icontains'],
        }
