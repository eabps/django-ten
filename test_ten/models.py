from django.db import models
from django.conf import settings
from django.urls import reverse

from ten.models import TenantBase, CollaborationBase, ForOneTenant, ForManyTenants


class Tenant(TenantBase):
    name = models.CharField(max_length=64, verbose_name='Name')

    class Meta:
        verbose_name = 'Tenant'
        verbose_name_plural = 'Tenants'

    def __str__(self):
        return "{}".format(self.name)
    
    def get_active_url(self):
        return reverse('tenant_active', args=[str(self.id)])


class Collaboration(CollaborationBase):
    
    class Meta:
        unique_together = ('tenant', 'user')
        verbose_name = 'Collaboration'
        verbose_name_plural = 'Collaborations'

    def __str__(self):
        return "{} - {}".format(self.user, self.tenant)
        

class Patient(ForManyTenants):
    name = models.CharField(max_length=32, verbose_name='Name')

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
    
    def __str__(self):
        return "{} {}".format(self.name, self.id)


class ScheduledService(ForOneTenant):
    patient = models.ForeignKey(Patient, verbose_name='Patient', on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='Date')

    class Meta:
        verbose_name = 'Scheduled Service'
        verbose_name_plural = 'Scheduled Services'
    
    def __str__(self):
        return "{}".format(self.patient)
