from rest_framework import permissions
from rest_framework.permissions import IsAdminUser, SAFE_METHODS

class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsAdminUserOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        is_admin = super(
            IsAdminUserOrReadOnly, 
            self).has_permission(request, view)
        # Python3: is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin

class IsPostMethod(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method.upper() == 'POST'


class IsSafeMethod(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method.upper() in ('OPTIONS', 'HEAD', 'GET')