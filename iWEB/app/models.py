# Dimitar: Location model

from django.db import models

# Location model
class Location(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    coordinates = models.IntegerField()
    information = models.CharField(max_length=200)
    report = models.CharField(max_length=201)
