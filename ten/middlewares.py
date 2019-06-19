# Ref: https://github.com/hugobessa/django-shared-schema-tenants/blob/dev/shared_schema_tenants/middleware.py

import threading

from django.contrib.auth.middleware import get_user as get_user_by_django
from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject
from django.conf import settings


def get_user_by_token(request):
    user = None
    authorization = request.META.get('HTTP_AUTHORIZATION', " ")

    try:
        token_flag = authorization.split(' ')[0]
        token = authorization.split(' ')[1]
    except IndexError:
        token_flag = None
        token = None

    print('TOKEN: ', token)
    print('FLAG: ', token_flag)

    if token_flag == 'simplejwt':
        from rest_framework_simplejwt.authentication import JWTAuthentication
        raw_token = JWTAuthentication().get_validated_token(token)
        user = JWTAuthentication().get_user(raw_token)
    elif token_flag == 'oauth':
        raise NotImplementedError('OAuth is not implemented yet at django-ten')
    elif token_flag =='hawk':
        raise NotImplementedError('Hawk is not implemented yet at django-ten')
    elif token_flag =='httpsignature':
        raise NotImplementedError('HTTP Signature Authentication is not implemented yet at django-ten')
    elif token_flag =='djoser':
        raise NotImplementedError('Djoser is not implemented yet at django-ten')
    elif token_flag =='django-rest-auth':
        raise NotImplementedError('Django-rest-auth is not implemented yet at django-ten')
    elif token_flag =='django-rest-framework-social-oauth2':
        raise NotImplementedError('django-rest-framework-social-oauth2 is not implemented yet at django-ten')
    elif token_flag =='django-rest-knox':
        raise NotImplementedError('django-rest-knox is not implemented yet at django-ten')
    elif token_flag =='drfpasswordless':
        raise NotImplementedError('drfpasswordless is not implemented yet at django-ten')
    
    if user is None: user = AnonymousUser()
    return user


def get_user(request):
    user = None

    http_authorization = request.META.get('HTTP_AUTHORIZATION', None)
    
    print('http_authorization: ', http_authorization)
    if http_authorization is not None:
        print('API')
        user = get_user_by_token(request)

    if hasattr(request, 'user') and user is None:
        print('SESSION')
        # from ten.helpers.models import User
        user = get_user_by_django(request)
        
    if user is None: user = AnonymousUser()
    print('get_user: ', user)
    
    return user


def get_tenant(request):
    #print('GET TENANT')
    tenant = None

    set_tenant = getattr(settings, 'SET_TENANT')

    if set_tenant == 'by_user':
        print(':::: TENANT BY USER ::::')
        user = get_user(request)

        if user:
            from ten.helpers.models import Collaboration
            try:
                collaboration = Collaboration.objects.get(user=user, _is_active=True)
                tenant = collaboration.tenant
            except Collaboration.DoesNotExist:
                pass
        
        else:
            print('NO USER')
    
    if set_tenant == 'by_url':

        print('request.get_host(): ', request.get_host())
        from ten.helpers.models import Tenant
        slug = settings.SLUG_TENANT(request.get_host())
        print('SLUG: ', slug)
        try:
            tenant = Tenant.objects.get(slug=slug)
        except Tenant.DoesNotExist:
            tenant = tenant
    
    return tenant


class TenantMiddleware:
    # https://docs.djangoproject.com/pt-br/2.1/topics/http/middleware/#writing-your-own-middleware

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
    
    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request = self.process_request(request)
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        return self.process_response(request, response)
    
    _threadmap = {}
  
    def process_request(self, request):
        request.set_tenant = getattr(settings, 'SET_TENANT')

        user = SimpleLazyObject(lambda: get_user(request))
        tenant = SimpleLazyObject(lambda: get_tenant(request))

        request.user = user
        
        self._threadmap[threading.get_ident()] = {'user': request.user, 'tenant': None}

        if request.set_tenant == 'by_user':
            print('BY USER')
            request.tenant = None if user.is_anonymous else tenant
        
        elif request.set_tenant == 'by_url':
            print('BY URL')
            request.tenant = tenant
        
        self._threadmap[threading.get_ident()]['tenant'] = request.tenant
        
        from ten.helpers.models import Collaboration
        if settings.SET_TENANT == 'by_url':
            if not user.is_anonymous:
                collaborations = Collaboration.objects.filter(user=user, _is_active=True)
                for c in collaborations:
                    c.deactivate(save=True)
        
        if tenant is not None:
            try:
                collaboration = Collaboration.objects.get(tenant=tenant, user=user)
                collaboration.activate()
            except (Collaboration.DoesNotExist, TypeError):
                pass

        return request

    
    def process_response(self, request, response):
        try:
            del request.tenant
        except AttributeError:
            pass

        try:
            del request.set_tenant
        except AttributeError:
            pass

        try:
            del self._threadmap[threading.get_ident()]
        except KeyError:
            pass
        
        return response
    
    def process_exception(self, request, exception):
        try:
            del self._threadmap[threading.get_ident()]
        except KeyError:
            pass
    
    @classmethod
    def get_current_tenant(cls):
        try:
            return cls._threadmap[threading.get_ident()]['tenant']
        except KeyError:
            return None
    
    @classmethod
    def get_current_user(cls):
        try:
            return cls._threadmap[threading.get_ident()]['user']
        except KeyError:
            return None
