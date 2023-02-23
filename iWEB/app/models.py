# Dimitar: Location model, Items model

from django.db import models
from django.contrib.auth.models import User

# Location model
class Location(models.Model):
    item_type = [('Fountain', 'Fountain'), ('BusStop', 'BusStop'), ('Bin', 'Bin')]
    type = models.CharField(max_length = 8, choices = item_type, default='Fountain')
    building = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()
    information = models.CharField(max_length=200)
    usable = models.BooleanField(default=True)

    # Makes the name of the item appear in the admin panel
    def __str__(self):
        return self.type
    


# Items model
class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    price = models.IntegerField()
    
    # Makes the name of the item appear in the admin panel
    def __str__(self):
        return self.name
