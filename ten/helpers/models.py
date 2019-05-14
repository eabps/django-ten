from django.conf import settings
from django.apps import apps as dj_apps


User = dj_apps.get_model(settings.AUTH_USER_MODEL)
Tenant = dj_apps.get_model(settings.TENANT_MODEL)
Collaboration = dj_apps.get_model(settings.COLLABORATION_MODEL)
