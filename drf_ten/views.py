from rest_framework.decorators import api_view

from . exceptions import TenantNotDefined


@api_view()
def tenant_not_defined(request):
	raise TenantNotDefined()
