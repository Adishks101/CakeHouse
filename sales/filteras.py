import django_filters
from .models import Sales


class SalesFilter(django_filters.FilterSet):
    class Meta:
        model = Sales
        fields = {
            'quantity_sold': ['exact', 'gte', 'lte'],
            'total_amount': ['exact', 'gte', 'lte']
        }
