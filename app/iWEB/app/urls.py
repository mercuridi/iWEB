"""
Module defining the web app's different directories and structures.
"""
from django.urls import path
from . import index, login
urlpatterns = [
    path('index', index.main,name='index'),
    path('register', login.register_request, name='register'),
    path('', login.login_request, name='login'),
]
