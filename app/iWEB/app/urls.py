from django.urls import path
from . import views
"""Module defining the web app's different directories and structures.
"""
urlpatterns = [
    path('test', views.test,name='test'),
    path('home', views.home, name='home'),
    path('addLocation', views.add_location, name='add-location'),
    path('register', views.register_request, name='register'),
    path("login", views.login_request, name="login")
]
