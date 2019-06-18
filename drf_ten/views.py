from rest_framework.decorators import api_view
from rest_framework.views import exception_handler

from . exceptions import TenantNotDefined


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code
        response.data['default_code'] = exc.default_code

    return response


@api_view()
def tenant_not_defined(request):
	raise TenantNotDefined()
