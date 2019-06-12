import functools

from django.conf import settings

from drf_ten.exceptions import TenantNotDefined


def tenant_required(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        request = args[0]
        try:
            if isinstance(request.tenant, type(None)):
                raise TenantNotDefined()
            else:
                return function(*args, **kwargs)
        except AttributeError:
            raise TenantNotDefined()
    return wrapper