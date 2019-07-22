from django.shortcuts import redirect
from django.conf import settings

from ten.exceptions import NotActivateTenant


def get_tenants(user=None):
    from ten.helpers.models import Collaboration
    
    if user is None: user = get_current_user()

    collaborations = Collaboration.objects.filter(user=user)
    return [c.tenant for c in collaborations]

def get_current_tenant():
    print('*** get_current_tenant in tenant.py ***')
    from ten.middlewares import TenantMiddleware
    return TenantMiddleware.get_current_tenant()


def get_current_user():
    from ten.middlewares import TenantMiddleware
    return TenantMiddleware.get_current_user()

"""
def set_currrent_tenant(user):
    '''
    Receiver user parameter.
    Instatiante the active tenant on database and register it on the session thread.
    If there is no active tenant in the database, redirect to tenant activate url.
    '''
    from ten.middlewares import TenantMiddleware    
    try:
        tenant = TenantMiddleware.set_tenant(user=user)
    except NotActivateTenant:
        #print('Redirect to Tenant URL')
        return redirect(settings.TENANT_URL)
    return TenantMiddleware.set_tenant(user=user)
"""