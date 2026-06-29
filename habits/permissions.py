from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnlyForPublic(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.is_public or obj.user == request.user
        return obj.user == request.user