from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

from drf_ten.decorators import tenant_required
from drf_ten.permissions import TenantRequiredPermissions

from test_ten.models import ScheduledService
from .serializers import ScheduledServiceSerializer


"""
from rest_framework.filters import BaseFilterBackend


class ByTenantFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):

        return queryset.filter(owner=request.user)
"""

@tenant_required
@api_view()
def fbv_test_get_tenant_decorator(request):
    return Response({"message":"Ok. sucess test tenant required decorator with FBV"})


class ScheduledServiceViewSet(ModelViewSet):
    queryset = ScheduledService.objects.all()
    serializer_class = ScheduledServiceSerializer
    #authentication_classes = (TokenAuthentication)
    permission_classes = (IsAuthenticated, TenantRequiredPermissions)

    def get_queryset(self):
        queryset = ScheduledService.original.all()
        from ten.helpers.tenant import get_current_tenant

        #return queryset.filter(tenant=get_current_tenant())
        return queryset
    

    def create(self, request, *args, **kwargs):
        return super(ScheduledServiceViewSet, self).create(request, *args, **kwargs)