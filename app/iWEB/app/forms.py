# Beth: Initial forms definitions

"""
Module defines the backend for the various forms we have in our app.
Integrates with the database via Django's hooks.
"""
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import TextInput
from django.contrib.auth.models import User
from .models import Location

# Create the form class.
class LocationForm(ModelForm):
    """Class defining the location submission form fields

    Args:
        ModelForm imported from Django (it just works!)
    """
    location_form = TextInput()

    # define the "meta" attributes of the form
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

    # define the "meta" attributes of the form
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # define how the form saves the data we input to it
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


