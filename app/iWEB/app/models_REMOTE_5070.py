# Dimitar: Location model, Items model
"""
Module defining the Location and Items models.
"""
from django.db import models
from django.contrib.auth.models import User

# Location model
class Location(models.Model):
    """Class defining the location model.
    """
    item_type = [('Fountain', 'Fountain'), ('BusStop', 'BusStop'), ('Bin', 'Bin')]
    type = models.CharField(max_length = 8, choices = item_type, default='Fountain')
    building = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()
    information = models.CharField(max_length=200)
    usable = models.BooleanField(default=True)

    # Makes the name of the item appear in the admin panel
    def __str__(self):
        return str(self.type)



# Items model
class Item(models.Model):
    """Class defining the item model."""
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    price = models.IntegerField()

    # Makes the name of the item appear in the admin panel
    def __str__(self):
        return str(self.name)
        
# Points system
class pointsSystem(models.Model):
    """Class defining the points system model."""
    streak = models.IntegerField(default = 0)
    score = models.IntegerField(default = 0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = 0)# type: ignore
    # Makes the name of the user appear in the admin panel
    def __str__(self):
        return str(self.user)
