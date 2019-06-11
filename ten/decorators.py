import functools

from django.shortcuts import render, redirect
from django.conf import settings


def tenant_required(function, url_to=settings.SELECT_TENANT_URL):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        request = args[0]
        try:
            if isinstance(request.tenant, type(None)):
                return redirect(url_to)
            else:
                return function(*args, **kwargs)
        except AttributeError:
            return redirect(url_to)
    return wrapper


def collaboration_required(function, is_active=None, url_to=settings.SELECT_TENANT_URL):
    """
    Require that request.user and request.tenant to be compatible
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        request = args[0]
        if isinstance(request.tenant, type(None)):
            return redirect(url_to)
        else:
            try:
                from ten.helpers.models import Collaboration
                collaboration = Collaboration.objects.get(tenant=request.tenant, user=request.user)
                if is_active is True and collaboration.is_active is False:
                    return redirect(url_to)
                return function(*args, **kwargs)
            except Collaboration.DoesNotExist:
                return redirect(url_to)
    return wrapper
