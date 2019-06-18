"""django_ten URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from test_ten.api import viewsets

from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

router = routers.SimpleRouter()
router.register(r'scheduledservices', viewsets.ScheduledServiceViewSet, basename='ScheduledService')

api_patterns = ([
    path('', include(router.urls)),
    path('fbv_test_get_tenant_decorator/', viewsets.fbv_test_get_tenant_decorator),

    # https://github.com/davesque/django-rest-framework-simplejwt#installation
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('drf-ten/', include('drf_ten.urls', namespace='drf_ten')),
], 'api')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('', include('test_ten.urls'), name='test_ten'),
    path('v1/', include(api_patterns, namespace='api')),
    #path('drf-ten/', include('drf_ten.urls', namespace='drf_ten')),
]
