from rest_framework.permissions import BasePermission

class CheckManager(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_manager:
            return True
        else:
            return False

