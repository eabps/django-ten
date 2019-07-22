from rest_framework import filters

from ten.models import ForTenantBase


class TenFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if ForTenantBase.mro()[0] in queryset.model.mro():
            queryset = queryset.filter(tenant=request.tenant)
        return queryset
        