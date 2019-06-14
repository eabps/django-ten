import functools

from django.shortcuts import redirect

from drf_ten.exceptions import TenantNotDefined



from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code
        response.data['default_code'] = exc.default_code

    return response


def tenant_required(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        request = args[0]
        try:
            if isinstance(request.tenant, type(None)):
                return redirect('drf_ten:tenant_not_defined')
                pass
            else:
                return function(*args, **kwargs)
        except AttributeError:
            return redirect('drf_ten:tenant_not_defined')
            pass
    return wrapper