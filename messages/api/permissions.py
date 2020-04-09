from rest_framework.permissions import BasePermission


class IsAuthenticate(BasePermission):
    def has_permission(self, request, view):
        return bool(request.auth)

class IsOwner(BasePermission):
    SAFE_METHODS = ('GET')

    def has_object_permission(self, request, view, obj):
        if request.method in self.SAFE_METHODS:
            return True

        return request.auth and obj.user_uuid == request.auth.get('uuid')