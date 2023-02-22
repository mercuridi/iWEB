#Dimitar: home view, addLocation view

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Location, Item
from .forms import LocationForm
# Create your views here.

def index(request):
    all_items = Item.objects.all
    all_locations = Location.objects.all
    return render(request, 'index.html', {'all_items': all_items, 'all_locations': all_locations})

def test(request):
    all_items = Item.objects.all
    all_locations = Location.objects.all
    return render(request, 'test.html', {'all_items': all_items, 'all_locations': all_locations})

def home(request):
    all_items = Item.objects.all
    all_locations = Location.objects.all
    return render(request, 'home.html', {'all_items': all_items, 'all_locations': all_locations})

def addLocation(request):
    submitted = False
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/addLocation?submitted=True')
    else:
        form = LocationForm
        if 'submitted' in request.GET:
            submitted = True
    form = LocationForm
    return render(request, 'addLocation.html', {'form': LocationForm, 'submitted': submitted})