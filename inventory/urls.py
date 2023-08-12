from django.urls import path
from .views import InventoryListView, InventoryDetailView, InventoryCreateView

urlpatterns = [
    path('', InventoryListView.as_view(), name='inventory-list'),
    path('create/', InventoryCreateView.as_view(), name='inventory-create'),
    path('<int:pk>/', InventoryDetailView.as_view(), name='inventory-detail'),
]
