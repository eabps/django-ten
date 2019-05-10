from django.contrib import admin
from . models import Tenant, Collaboration, Patient, ScheduledService


# Register your models here.
admin.site.register(Tenant)
admin.site.register(Collaboration)
admin.site.register(Patient)
admin.site.register(ScheduledService)
