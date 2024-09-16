from rest_framework.permissions import BasePermission


def permission_required(permission_name):
    class Permission(BasePermission):
        def has_permission(self, request, view):
            return request.user.has_perm(permission_name)

    return Permission


ViewInvestmentAccountPermission = permission_required("view_investment_account")
CreateInvestmentAccountPermission = permission_required("create_investment_account")
UpdateInvestmentAccountPermission = permission_required("update_investment_account")
DeleteInvestmentAccountPermission = permission_required("delete_investment_account")
PostTransactionPermission = permission_required("post_transaction")
