from django.conf import settings

from ten.exceptions import NotActivateTenant


def get_tenants(user=None):
    from ten.helpers.models import Collaboration
    
    if user is None: user = get_current_user()

    collaborations = Collaboration.objects.filter(user=user)
    return [c.tenant for c in collaborations]


def get_current_tenant():
    from ten.middlewares import TenantMiddleware
    return TenantMiddleware.get_current_tenant()


def get_current_user():
    from ten.middlewares import TenantMiddleware
    return TenantMiddleware.get_current_user()


def is_web():
    from ten.middlewares import TenantMiddleware
    return TenantMiddleware.is_web()
