# user/urls.py

from django.urls import path
from .views import CustomUserCreateView, CustomUserListView, CustomTokenObtainPairView, MyTokenRefreshView, \
    ChangePasswordView

urlpatterns = [
    path('create/', CustomUserCreateView.as_view(), name='user-create'),
    path('', CustomUserListView.as_view(), name='get-all-user'),
    path('change-password', ChangePasswordView.as_view(), name='change-password'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh', MyTokenRefreshView.as_view(), name="refresh-token")

]
