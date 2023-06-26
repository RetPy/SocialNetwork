from rest_framework.permissions import IsAuthenticated


class IsOwnerUser(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return bool(obj.user == request.user)


class IsCurrentUser(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return bool(obj == request.user)
