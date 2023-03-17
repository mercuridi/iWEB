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
    # Define possible location types and assign Fountain as the default
    item_type = [('Fountain', 'Fountain'), ('BusStop', 'BusStop'), ('Bin', 'Bin')]
    type = models.CharField(max_length = 8, choices = item_type, default='Fountain')
    # String to hold the building the location is in
    building = models.CharField(max_length = 100)
    # Longitude and latitude fields for location data
    longitude = models.FloatField(default = 0)
    latitude = models.FloatField(default = 0)
    # Information to keep general notes about location - directions, warnings, etc
    information = models.CharField(max_length = 200)
    # Boolean field for an easy way to keep track of if it's working or not
    usable = models.BooleanField(default = True)

    # Makes the name of the location and its building appear in the admin panel
    def __str__(self):
        return (f"{str(self.type)} ({str(self.building)})")

# Items model
class Item(models.Model):
    """Class defining the item model."""
    name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 100)
    price = models.IntegerField(default=0)

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
# This is where we 
class UserProfile(models.Model):
    """
    Class defining the model for user data.
    This is where user information not directly related to the account itself is kept.
    e.g. gamification data is stored here.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    streak = models.IntegerField(default = 0)
    score = models.IntegerField(default = 0)
    # fields to store the user's owned templates
    current_template = models.CharField(max_length = 50, default = "default")
    owned_templates = models.CharField(max_length = 150, default = "default")
    # boolean field for whether the user has completed a challenge
    challenge_done = models.BooleanField(default = False)
    current_challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, default = 1)

    # Makes the name of the user appear in the admin panel
    def __str__(self):
        return str(self.user)

# taken from https://www.turnkeylinux.org/blog/django-profile
# really useful snippet, causes profiles to be created when first referenced
# if they do not exist and allows referencing to profiles
# directly as user.profile instead of get_profile() or worse
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
