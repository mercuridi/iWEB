from django import forms
from django.forms import ModelForm
from .models import Location

# Create the form class.
class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ['type', 'building', 'longitude', 'latitude', 'information', 'usable']