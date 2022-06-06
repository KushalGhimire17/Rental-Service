from rest_framework import permissions

class IsUserOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        
        if request.user.is_staff:
            return True

        try:
            if request.user.phone:
                return obj.phone == request.user.phone
        except AttributeError:
            return False
        return False