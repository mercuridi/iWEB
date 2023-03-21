"""
Python file representing 
"""
import json
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Location, Item, UserProfile
from .forms import LocationForm
from .utils.mapUtilities import read_map

def main(request):
    """
    
    """
    
    context = {
    }

    return render(request, 'help.html', context)
