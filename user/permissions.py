# permissions.py

from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user and (request.user.user_type == 'admin')


class IsFranchiseUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.user_type == 'franchise')


class IsFranchiseOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.user_type == 'franchise')

    def has_object_permission(self, request, view, obj):
        # Allow if the authenticated user is the owner of the franchise
        return request.user.franchise == obj.franchise


class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
