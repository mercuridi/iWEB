"""
Module defining the web app's different directories and structures.
"""
from django.urls import path
from . import debug, index, login, help
urlpatterns = [
    path('index', index.main,name='index'),
    path('home', debug.home, name='home'),
    path('register', login.register_request, name='register'),
    path('', login.login_request, name='login'),
    path('map', debug.map_view, name='map'),
    path('help', help.main, name='help'),
]
