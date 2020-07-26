from rest_framework import permissions


class AllowCreations(permissions.BasePermission):
    def has_permission(self, request, view):
        # For creation requests, POST, allow
        if request.method == "POST":
            return True
        return False


class NoDeletes(permissions.BasePermission):
    """Doesn't allow deletes for the resource."""

    def has_permission(self, request, view):
        if request.method == "DELETE":
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return False
        return True
