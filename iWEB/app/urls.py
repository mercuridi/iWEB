from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('test', views.test,name='test'),
    path('home', views.home, name='home'),
    path('addLocation', views.addLocation, name='add-location'),
]
