from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

from drf_ten.decorators import tenant_required
from drf_ten.permissions import TenantRequiredPermissions

from test_ten.models import ScheduledService
from .serializers import ScheduledServiceSerializer


@tenant_required
@api_view()
def fbv_test_get_tenant_decorator(request):
    schedule_services = ScheduledService.objects.all()
    schedule_service_serializer = ScheduledServiceSerializer(schedule_services, many=True)
    data = schedule_service_serializer.data
    return Response(data)


class ScheduledServiceViewSet(ModelViewSet):
    queryset = ScheduledService.objects.all()
    serializer_class = ScheduledServiceSerializer
    #authentication_classes = (TokenAuthentication)
    permission_classes = (IsAuthenticated, TenantRequiredPermissions)

    """def get_queryset(self):
        queryset = ScheduledService.original.all()
        from ten.helpers.tenant import get_current_tenant

        return queryset.filter(tenant=get_current_tenant())"""
    

    def create(self, request, *args, **kwargs):
        return super(ScheduledServiceViewSet, self).create(request, *args, **kwargs)