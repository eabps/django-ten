from django.urls import path

from . import views


app_name = 'drf_ten'

urlpatterns = [
    path('tenant-not-defined/', views.tenant_not_defined, name='tenant_not_defined'),
]
