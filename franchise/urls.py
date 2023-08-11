from django.urls import path
from .views import FranchiseListView, FranchiseDetailView

urlpatterns = [
    path('', FranchiseListView.as_view(), name='franchise-list'),
    path('<int:pk>/', FranchiseDetailView.as_view(), name='franchise-detail'),
]
