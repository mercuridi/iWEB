"""
Module defining the web app's different directories and structures.
"""
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index,name='index'),
    path('home', views.home, name='home'),
    path('register', views.register_request, name='register'),
    path("login", views.login_request, name="login"),
    path('map', views.map_view, name='map'),
]
