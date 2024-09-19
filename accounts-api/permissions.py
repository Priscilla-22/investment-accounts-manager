from rest_framework import permissions


class IsViewOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.account_type == "view_only"


class IsFullAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.account_type == "full_access"


class IsPostOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.account_type == "post_only"
