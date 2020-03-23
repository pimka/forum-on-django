from rest_framework.permissions import BasePermission

class IsAuth(BasePermission):
    SAFE_METHODS = ('POST', )

    def has_permission(self, request, view):
        if request.method in self.SAFE_METHODS or request.auth:
            return True
        return False