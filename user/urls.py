# user/urls.py

from django.urls import path
from .views import CustomUserCreateView,CustomUserListView

urlpatterns = [
    path('create/', CustomUserCreateView.as_view(), name='user-create'),
    path('',CustomUserListView.as_view(),name='get-all-user'),
]
