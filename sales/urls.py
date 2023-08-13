from django.urls import path
from .views import SalesListView, SalesDetailView, SaleCreateView

urlpatterns = [
    path('', SalesListView.as_view(), name='sales-list'),
    path('create/', SaleCreateView.as_view(), name="sale_create"),
    path('<int:pk>/', SalesDetailView.as_view(), name='sales-detail'),
]
