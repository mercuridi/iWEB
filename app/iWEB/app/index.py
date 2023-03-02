from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Location, Item
from .forms import LocationForm
from django.contrib.auth.models import User
from .utils.mapUtilities import read_map

def main(request):
    """This is the main page - everything but the login/register screen should be in this view going forward"""
    userList = User.objects.values()
    locList = Location.objects.values()
    itemList = Item.objects.all

    #add location
    submitted = False
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/addLocation?submitted=True') #This should probably be changed to avoid redirects to a dead page
    else:
        form = LocationForm
        if 'submitted' in request.GET:
            submitted = True
    form = LocationForm

    #map stuff
    fountain_locations = Location.objects.filter(type='Fountain')
    bus_stop_locations = Location.objects.filter(type='BusStop')
    bin_locations = Location.objects.filter(type='Bin')
    
    fountain_coordinates = []
    bus_stop_coordinates = []
    bin_coordinates = []
    
    for fountain in fountain_locations:
        fountain_coordinates.append([fountain.latitude, fountain.longitude, fountain.building, fountain.information])
    for bus_stop in bus_stop_locations:
        bus_stop_coordinates.append([bus_stop.latitude, bus_stop.longitude, bus_stop.building, bus_stop.information])
    for bin in bin_locations:
        bin_coordinates.append([bin.latitude, bin.longitude, bin.building, bin.information])
    
    map = read_map()
    
    context = {
    'fountain_locations': fountain_coordinates,
    'bus_stop_locations': bus_stop_coordinates,
    'bin_locations': bin_coordinates,
    'maze': map,
    'colour1': ["#4a120f"],
    'points': 256, # TODO: CHANGE THIS PLEASE
    'item_list': itemList,
    'scores': userList,
    'closest_things': locList,
    'location_form': LocationForm,
    'submitted': submitted
    } 
    print(bin_coordinates)
    return render(request, 'index.html', context)