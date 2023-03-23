#Dash : This file
from django.test import TestCase
from django.test import Client
from app.models import User
from django.urls import reverse


# Kai: Try using the Client from django.test?
# Imported for you ^^ https://docs.djangoproject.com/en/4.1/topics/testing/tools/
c = Client()

class BaseTest(TestCase):
    def setUp(self):
        self.register_url=reverse('register')
        self.user={
            'user':'username2', 
            'email':'anotheremail@email.com', 
            'password1':'password1', 
            'password2':'password1'
        }
        return super().setUp()

class RegisterTest(BaseTest):
    def test_can_view_page(self):
        response=self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200) #page is successfully accessed
        self.assertTemplateUsed(response, 'register.html') #template is successfully used

    # places test values into the registration form
    def test_can_register_user(self):
        response=self.client.post(self.register_url,self.user,format='/html')
        self.assertEqual(response.status_code,200)

class LoginClass(TestCase):
    def setUp(self):
        self.login_url=reverse('login')
        self.user={
            'username':'username', 
            'email':'email@email.com', 
            'password1':'password12', 
            'password2':'password12'
        }
        return super().setUp()

class LoginTest(LoginClass, BaseTest ):
    def test_can_view_page(self):
        response=self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200) #page is successfully accessed
        self.assertTemplateUsed(response, 'login.html') #template is successfully used
    def test_login_success(self):
        self.client.post(self.register_url,self.user,format='/html')
        user = User.objects.filter(email=self.user['email']).all()
        user.is_active=True
        response = self.client.post(self.login_url, self.user, format='/html')
        self.assertEqual(response.status_code, 200)