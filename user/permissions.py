# permissions.py

from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.user_type == 'admin')


class IsFranchiseUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.user_type == 'franchise')


class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user
