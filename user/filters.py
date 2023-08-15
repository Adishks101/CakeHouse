import django_filters
from .models import CustomUser


class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = CustomUser
        fields = {
            'user_type': ['exact'],
            'email': ['exact', 'gte', 'lte'],
            'created_at': ['exact', 'gte', 'lte'],
            'first_name': ['exact', 'icontains']
        }
