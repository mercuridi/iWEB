from django import forms
from django.forms import ModelForm
from .models import Location
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create the form class.
class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ['type', 'building', 'longitude', 'latitude', 'information', 'usable']
        
class NewUserForm(UserCreationForm):
    streak = forms.IntegerField(initial = 0, disabled = True)
    points = forms.IntegerField(initial = 0, disabled = True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','streak', 'points']

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user