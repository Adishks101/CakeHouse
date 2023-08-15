from django.urls import path
from .views import InventoryListView, InventoryDetailView, InventoryCreateView, InventoryListViewByFranchise

urlpatterns = [
    path('', InventoryListView.as_view(), name='inventory-list'),
    path('create/', InventoryCreateView.as_view(), name='inventory-create'),
    path('franchise/<int:franchise>/', InventoryListViewByFranchise.as_view(), name='franchise-wise-inventory'),
    path('<int:pk>/', InventoryDetailView.as_view(), name='inventory-detail'),
]
