# user/urls.py

from django.urls import path
from .views import CustomUserCreateView, CustomUserListView, CustomTokenObtainPairView, MyTokenRefreshView, \
    ChangePasswordView, CurrentUserView, AdminChangePasswordView, CustomUserUpdateView

urlpatterns = [
    path('create/', CustomUserCreateView.as_view(), name='user-create'),
    path('', CustomUserListView.as_view(), name='get-all-user'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('admin-change-password/', AdminChangePasswordView.as_view(), name='admin-change-password'),
    path('update/<int:pk>/', CustomUserUpdateView.as_view(), name='update-user'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('current-user/', CurrentUserView.as_view(), name='current-user'),
    path('token/refresh', MyTokenRefreshView.as_view(), name="refresh-token")

]
