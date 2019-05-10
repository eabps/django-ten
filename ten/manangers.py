from django.db import models

from ten.helpers.tenant import get_current_tenant, get_current_user


class ForOneTenantManager(models.Manager):
    def get_original_queryset(self, *args, **kwargs):
        return super(ForOneTenantManager, self).get_queryset(*args, **kwargs)

    def get_queryset(self, tenant=None, *args, **kwargs):
        tenant = get_current_tenant() if tenant is None else tenant

        if tenant:
            return super(ForOneTenantManager, self).get_queryset(*args, **kwargs).filter(tenant=tenant)
        
        return super(ForOneTenantManager, self).get_queryset(*args, **kwargs).none()


class ForManyTenantsManager(models.Manager):
    def get_original_queryset(self, *args, **kwargs):
        return super(ForOneTenantManager, self).get_queryset(*args, **kwargs)

    def get_queryset(self, user=None, tenant=None, *args, **kwargs):
        tenant = get_current_tenant() if tenant is None else tenant
        if tenant:
            from . helpers.collaboration import Collaboration
            collaborations = Collaboration.original.filter(user=tenant.owner, owner=True)
            tenants = set([c.tenant for c in collaborations])
            return super(ForManyTenantsManager, self).get_queryset(*args, **kwargs).filter(tenant__in=tenants)
        
        return super(ForManyTenantsManager, self).get_queryset(*args, **kwargs).none()


class CollaborationBaseManager(models.Manager):    
    def get_original_queryset(self, *args, **kwargs):
        return super(CollaborationBaseManager, self).get_queryset(*args, **kwargs)
    
    def get_queryset(self, user=None, *args, **kwargs):
        user = get_current_user() if user is None else user

        print('UUSER: ', user)

        if user and not user.is_anonymous:
            return super(CollaborationBaseManager, self).get_queryset(*args, **kwargs).filter(user=user)
        
        return super(CollaborationBaseManager, self).get_queryset(*args, **kwargs).none()
