from rest_framework import permissions


class IsViewOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            # View-only users should not be able to post transactions
            return False
        return True


class IsFullAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        return True


class IsPostOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Post-only users should only be able to create transactions, not view them
        if request.method == "POST":
            return True
        return False
