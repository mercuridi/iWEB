""" Module defines the backend for the various forms we have in our app.
    Integrates with the database via Django's hooks.
"""
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Location

# Create the form class.
class LocationForm(ModelForm):
    """Class defining the location submission form fields

    Args:
        ModelForm imported from Django (it just works!)
    """
    class Meta:
        model = Location
        fields = ['type', 'building', 'longitude', 'latitude', 'information', 'usable']


class NewUserForm(UserCreationForm):
    """Class defining the form to create a new user

    Args:
        UserCreationForm imported from Django (also just works!)
    Returns:
        A new user into the database upon a valid submission
    """

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
