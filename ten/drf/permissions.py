from rest_framework import permissions

from . exceptions import TenantNotDefined


class TenantRequiredPermissions(permissions.BasePermission):
    """
    Check if tenant is defined. If not, raise TenantNotDefined exception
    """

    def has_permission(self, request, view):
        if request.tenant == None:
            raise TenantNotDefined()
        else:
            return True