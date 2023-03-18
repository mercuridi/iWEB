# Dimitar: Location model, Items model
# Kai: Challenges model, UserProfile model
"""
Module defining the Location, Items, Challenge, and UserProfile models.
"""
from django.db import models
from django.contrib.auth.models import User

# Location model
class Location(models.Model):
    """Class defining the location model."""
    item_type = [('Fountain', 'Fountain'), ('BusStop', 'BusStop'), ('Bin', 'Bin')]
    type = models.CharField(max_length = 8, choices = item_type, default='Fountain')
    building = models.CharField(max_length = 100)
    longitude = models.FloatField()
    latitude = models.FloatField()
    information = models.CharField(max_length = 200)
    usable = models.BooleanField(default = True)

    # Makes the name of the location and its building appear in the admin panel
    def __str__(self):
        return (f"{str(self.type)} ({str(self.building)})")

# Items model
class Item(models.Model):
    """Class defining the item model."""
    name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 100)
    price = models.IntegerField()

    # Makes the name of the item appear in the admin panel
    def __str__(self):
        return str(self.name)

class Challenge(models.Model):
    """Class defining the challenges that exist in the app."""
    name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 200)
    difficulty = models.IntegerField(default = 1)
    
    def __str__(self):
        return str(self.name)

# Data related to users (not account information!)
class UserProfile(models.Model):
    """Class defining the model for user data."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    streak = models.IntegerField(default = 0)
    score = models.IntegerField(default = 0)
    current_template = models.CharField(max_length = 50, default = "default")
    owned_templates = models.CharField(max_length = 150, default = "default")
    challenge_done = models.BooleanField(default = False)
    current_challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, default = 1)

    # Makes the name of the user appear in the admin panel
    def __str__(self):
        return str(self.user)

