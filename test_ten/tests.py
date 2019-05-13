from django.test import TestCase, RequestFactory, override_settings, Client
from django.contrib.auth.models import AnonymousUser, User
from django.shortcuts import redirect

from ten.helpers.tenant import get_current_tenant, get_current_user
from ten.middlewares import TenantMiddleware

from test_ten import views
from test_ten.models import Tenant, Collaboration


class SimpleTest(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.anonymous_user = AnonymousUser()
        self.user = User.objects.create(
            username='jacob',
            email='jacob@…',
            password='top_secret'
        )
        self.orphan_tenant = Tenant.objects.create(name='Orphan Tenant', slug='orphan')
        self.one_tenant = Tenant.objects.create(name='One Tenant', slug='one')

        self.collaboration = Collaboration.objects.create(
            tenant = self.one_tenant,
            user = self.user,
            owner = True
        )
    
    def test_home(self):
        request = self.request_factory.get('home')
        
        # With Anonymous User
        request.user = self.anonymous_user
        response = views.home(request)
        self.assertEqual(200, response.status_code)
    
    def test_tenant_required(self):
        """
        test views with decorator @tenant_required
        """

        # with announimous user and withless actived tenant
        client = Client()
        response = client.get('/patient/create/')
        self.assertRedirects(response, '/tenant/select/')

        # with user and withless actived tenant
        client = Client()
        
        request = self.request_factory.get('/patient/create/')
        request.user = self.user
        client.request = request
        response = client.get('/patient/create/')
        self.assertRedirects(response, '/tenant/select/')

    # CORRENT TENANT
    
    # TEST CORRENT USER

    # TEST DATA ISOLATION

    # TEST TOKEN

    # TEST DINAMIC URL

    # TEST SETTING CONFIG