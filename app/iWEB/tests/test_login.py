from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse


# Kai: Try using the Client from django.test?
# Imported for you ^^ https://docs.djangoproject.com/en/4.1/topics/testing/tools/
c = Client()


class RegisterClass(TestCase):
    def setUp(self):
        self.register_url=reverse('register')
        self.user={
            'username':'username', 
            'email':'email@email.com', 
            'password1':'password', 
            'password2':'password'
        }
        return super().setUp()

class RegisterTest(RegisterClass):
    def test_can_view_page(self):
        response=self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200) #page is successfully accessed
        self.assertTemplateUsed(response, 'register.html') #template is successfully used

    def test_can_register_user(self):
        response=self.client.post(self.register_url,{},format='')
        self.assertEqual(response.status_code,302)