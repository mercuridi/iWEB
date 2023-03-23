# Dimitar: Location model, Items model
# Kai: Challenges model, UserProfile model, Usage model, 
#       file formatting for readability
"""
Module defining the Location, Items, Challenge, and UserProfile models.
"""
from django.db import models
from django.contrib.auth.models import User

# Location model
class Location(models.Model):
    """Class defining the location model."""
    item_type   = [('Fountain', 'Fountain'), ('BusStop', 'BusStop'), ('Bin', 'Bin')]
    type        = models.CharField(max_length = 8, choices = item_type, default='Fountain')
    building    = models.CharField(max_length = 100)
    information = models.CharField(max_length = 200)
    longitude   = models.FloatField(default=0)
    latitude    = models.FloatField(default=0)
    usable      = models.BooleanField(default = True)

    # Makes the name of the location and its building appear in the admin panel
    def __str__(self):
        return f"{str(self.type)} ({str(self.building)})"

# Items model
class Item(models.Model):
    """Class defining the item model. Mostly used for themes."""
    name        = models.CharField(max_length = 50)
    description = models.CharField(max_length = 100)
    price       = models.IntegerField(default = 0)

    # Makes the name of the item appear in the admin panel
    def __str__(self):
        return str(self.name)

# Challenge model
class Challenge(models.Model):
    """Class defining the challenges that exist in the app."""
    name        = models.CharField(max_length = 50)
    description = models.CharField(max_length = 200)
    type        = models.CharField(max_length=50)
    difficulty  = models.IntegerField(default = 1)


    # Makes the challenge name appear in the admin panel
    def __str__(self):
        return str(self.name)

# Data related to users (not account information!)
class UserProfile(models.Model):
    """Class defining the model for user data."""
    # The user column defines the profile as an extension of the User model.
    # The current_challenge column defines a many-to-one relationship between users and challenges.
    user                = models.OneToOneField(User, on_delete=models.CASCADE)
    points_wallet       = models.IntegerField(default = 0)
    points_this_week    = models.IntegerField(default = 0)
    points_lifetime     = models.IntegerField(default = 0)
    streak              = models.IntegerField(default = 0)
    current_template    = models.CharField(max_length =  50, default = "default")
    owned_templates     = models.CharField(max_length = 150, default = "default")
    challenge_done      = models.BooleanField(default = False)
    current_challenge   = models.ForeignKey(Challenge, on_delete=models.CASCADE, default = 1)

    # Makes the name of the user appear in the admin panel
    def __str__(self):
        return str(self.user)

# taken from https://www.turnkeylinux.org/blog/django-profile
# really useful snippet, causes profiles to be created when first referenced
# if they do not exist and allows referencing to profiles
# directly as user.profile instead of get_profile() or worse
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class Usage(models.Model):
    """Class defining the model that tracks usage across the app."""
    fountains_used  = models.IntegerField(default=0)
    bus_stops_used  = models.IntegerField(default=0)
    bins_used       = models.IntegerField(default=0)
    total_used      = models.IntegerField(default=0)