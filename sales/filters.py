import django_filters
from .models import Sales


class SalesFilter(django_filters.FilterSet):
    sale_date = django_filters.DateFromToRangeFilter(field_name='sale_date')

    class Meta:
        model = Sales
        fields = {
            'total_amount': ['exact', 'gte', 'lte'],
            'payment_mode': ['exact', 'icontains']
        }
