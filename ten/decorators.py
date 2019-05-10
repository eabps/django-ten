import functools

from django.shortcuts import render, redirect
from django.conf import settings


def tenant_required(function, url_to=settings.SELECT_TENANT_URL):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        request = args[0]
        if isinstance(request.tenant, type(None)):
            return redirect(url_to)
        else:
            return function(*args, **kwargs)
    return wrapper
    