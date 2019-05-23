from django.conf import settings
from django.db import models, transaction

from ten.helpers.tenant import get_current_tenant, get_current_user

from . manangers import ForOneTenantManager, ForManyTenantsManager, CollaborationBaseManager


class ForOneTenant(models.Model):
    '''
    Abstract class for class with relation many to one (tenants).
    '''
    tenant = models.ForeignKey(settings.TENANT_MODEL, verbose_name='Tenant', on_delete=models.CASCADE)
    
    objects = ForOneTenantManager()
    original = models.Manager() # The default django model manager.

    class Meta:
        abstract = True
    
    def save(self, tenant=None, *args, **kwargs):
        if tenant is None: self.tenant = get_current_tenant()
        super().save(*args, **kwargs)


class ForManyTenants(models.Model):
    # Falta sobrescrever o add (ob.tenants.add()) de modo que seja possível add somente tenants do mesmo proprientário
    '''
    Abstract class for class with relation many to many (tenants).
    '''


    tenants = models.ManyToManyField(settings.TENANT_MODEL, verbose_name='Tenant')
    #is_shared = models.BooleanField(default=True, verbose_name='Is shared')

    objects = ForManyTenantsManager()
    original = models.Manager() # The default django model manager.

    class Meta:
        abstract = True
    
    def save(self, add_current_tenant=True, *args, **kwargs):
        super().save(*args, **kwargs)

        if add_current_tenant:
            if get_current_tenant():
                self.tenants.add(get_current_tenant())
            else:
                from ten.helpers.models import Tenant
                self.delete()
                tenant = Tenant()
                raise ValueError("get_current_tenant() returned None. To save an instance of {} unlinked from {}, use instance.save(add_current_tenant=False)".format(self.__class__, tenant.__class__))


class CollaborationBase(models.Model):
    tenant = models.ForeignKey(settings.TENANT_MODEL, on_delete=models.CASCADE, verbose_name='Tenant')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='User')
    owner = models.BooleanField(default=False, verbose_name='Owner')
    _is_active = models.BooleanField(default=False, verbose_name='Is Active')

    objects = CollaborationBaseManager()
    original = models.Manager() # The default django model manager.

    class Meta:
        abstract = True
        unique_together = ('tenant', 'user')
        verbose_name = 'Collaboration'
        verbose_name_plural = 'Collaborations'
    
    @property
    def is_active(self):
        return self._is_active
    
    def deactivate(self, save=False):
        self._is_active = False
        
        if save is True:
            self.save()
    
    @transaction.atomic
    def bulk_deactivate(self, collaborations):
        for c in collaborations:
            c.deactivate(save=True)
    
    def activate(self, user=None):
        if user is None: user = get_current_user()

        from ten.helpers.models import Collaboration
        
        collaborations = Collaboration.objects.filter(user=user, _is_active=True)
        self.bulk_deactivate(collaborations)

        self._is_active = True
        self.save()
    
    def save(self, *args, **kwargs):
        # CREATE OR UPDATE
        if kwargs.get('tenant'): self.tenant = kwargs.get('tenant')
        if kwargs.get('user'): self.user = kwargs.get('user')

        from ten.helpers.models import Collaboration

        try:
            if self.user is None: self.user = get_current_user()
        except Collaboration.user.RelatedObjectDoesNotExist:
            self.user = get_current_user()

        super().save(*args, **kwargs)


class TenantBase(models.Model):
    slug = models.SlugField(max_length=64, null=True, unique=True)

    class Meta:
        abstract = True
        verbose_name = 'Tenant'
        verbose_name_plural = 'Tenants'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
        super().save(*args, **kwargs)

    def get_unique_slug(self):
        import uuid
        return str(uuid.uuid4())

    def activate(self, user=None):
        from ten.helpers.models import Collaboration
        user = get_current_user() if user is None else user
        collaboration = Collaboration.objects.get(tenant=self, user=user)
        collaboration.activate(user)
    
    @property
    def owner(self):
        from ten.helpers.models import Collaboration
        collaboration = Collaboration.original.get(tenant=self, owner=True)
        owner = collaboration.user
        return owner
