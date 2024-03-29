from django.urls import path
from .views import FranchiseListView, FranchiseDetailView, FranchiseCreateView, FranchiseSelfView

urlpatterns = [
    path('', FranchiseListView.as_view(), name='franchise-list'),
    path('create/', FranchiseCreateView.as_view(), name='franchise-create'),
    path('<int:pk>/', FranchiseDetailView.as_view(), name='franchise-detail'),
    path('self/', FranchiseSelfView.as_view(), name='user-franchise'),
]
