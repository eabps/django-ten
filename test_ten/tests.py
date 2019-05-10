from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from django.shortcuts import redirect

from test_ten import views


class SimpleTest(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.anonymous_user = AnonymousUser()
        self.user = User.objects.create(
            username='jacob',
            email='jacob@…',
            password='top_secret'
        )
    
    def test_home(self):
        request = self.request_factory.get('home')
        
        # With Anonymous User
        request.user = self.anonymous_user
        response = views.home(request)
        self.assertEqual(200, response.status_code)
    
    """
    def test_set_create_tenant(self):
        request = self.request_factory.post('')
    """
        


