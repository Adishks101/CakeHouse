# permissions.py

from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsRegularUser(BasePermission):
    def has_permission(self, request, view):
        return request.user
