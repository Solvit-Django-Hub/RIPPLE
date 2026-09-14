from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsProjectOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated

        
        if request.method == 'POST':
            return (
                request.user and
                request.user.is_authenticated and
                request.user.role in ['analyst', 'admin']
            )

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        
        if request.method in SAFE_METHODS:
            return True

        
        return obj.owner == request.user or request.user.role == 'admin'