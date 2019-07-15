from rest_framework import filters


class TenantFilter(filters.BaseFilterBackend):
    """
    Filter that only allows return objects by tenant
    """

    def filter_queryset(self, request, queryset, view):
        print(';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;')
        print(request.tenant)
        return queryset.filter(tenant=request.tenant)
