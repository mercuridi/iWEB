from django.test import TestCase
from django.contrib.auth.models import User

class LoginClass(TestCase):
    @classmethod
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
    def test_login(self):
        # login
        response = self.client.post('/login/', self.credentials, follow=True)      
        # should be logged in now
        self.assertTrue(response.context['user'].is_authenticated)
    pass