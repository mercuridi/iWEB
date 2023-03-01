from django.urls import path
from . import views
"""Module defining the web app's different directories and structures.
"""
urlpatterns = [
    path('', views.index,name='index'),
    path('home', views.home, name='home'),
    path('register', views.register_request, name='register'),
    path("login", views.login_request, name="login")
]
