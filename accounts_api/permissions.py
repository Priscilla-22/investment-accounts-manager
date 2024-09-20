from rest_framework import permissions


class IsViewOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return False
        return True


class IsFullAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        return True


class IsPostOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        return False
