from django.db import models

from ten.helpers.tenant import get_current_tenant, get_current_user


class ForOneTenantManager(models.Manager):
    def get_original_queryset(self, *args, **kwargs):
        print('>> get_original_queryset')
        return super(ForOneTenantManager, self).get_queryset(*args, **kwargs)

    def get_queryset(self, tenant=None, *args, **kwargs):
        print('*** MANAGER get_queryset by ForOneTenantManager ***')
        tenant = get_current_tenant() if tenant is None else tenant

        print('Tenant IN MANAGER: ', tenant)

        #if tenant:
        #    return super().get_queryset(*args, **kwargs).filter(tenant=tenant)
        
        return super().get_queryset(*args, **kwargs).filter(tenant=tenant)


class ForManyTenantsManager(models.Manager):
    def get_original_queryset(self, *args, **kwargs):
        return super(ForManyTenantsManager, self).get_queryset(*args, **kwargs)

    def get_queryset(self, user=None, tenant=None, *args, **kwargs):
        if tenant is None: tenant = get_current_tenant()
        if tenant:
            from . helpers.models import Collaboration
            collaborations = Collaboration.original.filter(user=tenant.owner, owner=True)
            tenants = set([c.tenant for c in collaborations])
            return super(ForManyTenantsManager, self).get_queryset(*args, **kwargs).filter(tenants__in=tenants)
        
        return super(ForManyTenantsManager, self).get_queryset(*args, **kwargs).none()
    
    def create(self, **kwargs):
        """
        Create a new object with the given kwargs, saving it to the database
        and returning the created object.
        """
        try:
            add_current_tenant = kwargs.pop('add_current_tenant')
        except KeyError:
            add_current_tenant = True
        
        obj = self.model(**kwargs)
        self._for_write = True
        obj.save(force_insert=True, using=self.db, add_current_tenant=add_current_tenant)
        return obj


class CollaborationBaseManager(models.Manager):    
    def get_original_queryset(self, *args, **kwargs):
        return super(CollaborationBaseManager, self).get_queryset(*args, **kwargs)
    
    def get_queryset(self, user=None, *args, **kwargs):
        #print(get_current_user())
        user = get_current_user() if user is None else user

        #print('UUSER: ', user)

        if user and not user.is_anonymous:
            return super(CollaborationBaseManager, self).get_queryset(*args, **kwargs).filter(user=user)
        
        return super(CollaborationBaseManager, self).get_queryset(*args, **kwargs).none()
