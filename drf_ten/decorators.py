import functools

from django.shortcuts import redirect

from drf_ten.exceptions import TenantNotDefined

from django.conf import settings


DRF_TEN_NAMESPACE = getattr(settings, 'DRF_TEN_NAMESPACE', 'drf_ten')

def tenant_required(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        request = args[0]
        try:
            if isinstance(request.tenant, type(None)):
                return redirect("{}:tenant_not_defined".format(DRF_TEN_NAMESPACE))
            else:
                return function(*args, **kwargs)
        except AttributeError:
            return redirect("{}:tenant_not_defined".format(DRF_TEN_NAMESPACE))
    return wrapper