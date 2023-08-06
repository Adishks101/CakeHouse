from django.urls import path
from .views import InventoryListView, InventoryDetailView

urlpatterns = [
    path('', InventoryListView.as_view(), name='inventory-list'),
    path('<int:pk>/', InventoryDetailView.as_view(), name='inventory-detail'),
]
