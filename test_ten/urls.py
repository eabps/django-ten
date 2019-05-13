from django.contrib import admin
from django.urls import path

from test_ten import views


urlpatterns = [
    path('', views.home, name='home'),
    path('tenant/select/', views.home, name='tenant_select'),
    path('account/create/', views.account_create, name='account_create'),
    path('tenant/create/', views.tenant_create, name='tenant_create'),
    path('patient/create/', views.patient_create, name='patient_create'),
    path('scheduled-service/create/', views.scheduled_service_create, name='scheduled_service_create'),
    path('scheduled-service/list/', views.scheduled_service_list, name='scheduled_service_list'),
    path('tenant/active/<int:pk>/', views.tenant_active, name='tenant_active'),
]
