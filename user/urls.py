# user/urls.py

from django.urls import path
from .views import CustomUserCreateView,CustomUserListView, CustomTokenObtainPairView

urlpatterns = [
    path('create/', CustomUserCreateView.as_view(), name='user-create'),
    path('',CustomUserListView.as_view(),name='get-all-user'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

]
