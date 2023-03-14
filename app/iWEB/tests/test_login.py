from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User


# Kai: Try using the Client from django.test?
# Imported for you ^^ https://docs.djangoproject.com/en/4.1/topics/testing/tools/
c = Client()

class LoginClass(TestCase):
    #@classmethod
    #def setUp(self):
    #    self.credentials = {
    #        'username': 'testuser',
    #        'password': 'secret'}
    #    User.objects.create_user(**self.credentials)
    #def test_login(self):
    #    # login
    #    response = self.client.post('/login/', self.credentials, )      
    #    # should be logged in now
    #    self.assertTrue(response.context['user'].is_authenticated)
    pass