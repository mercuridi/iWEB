from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Location, Item, UserProfile
from .forms import LocationForm
from .utils.mapUtilities import read_map
import json

def main(request):
    """This is the main page - everything but the login/register screen should be in this view going forward"""

    # load user info from request
    current_user = request.user
    current_user_data = current_user.profile
    
    #add location
    submitted = False
    if request.method == "POST":
        # handle points increases
        data = json.loads(request.body)
        points = data.get("points")
        current_user_data.score += points
        current_user_data.save()

        # handle location form submissions
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/addLocation?submitted=True') #This should probably be changed to avoid redirects to a dead page
    else:
        form = LocationForm
        if 'submitted' in request.GET:
            submitted = True
    form = LocationForm

    # context setup
    all_locations = get_locations()
    map = read_map()
    leaderboard = get_leaderboard()
    
    # TODO does this actually give us the closest things?
    loc_list = Location.objects.values()
    item_list = Item.objects.values().order_by("price")
    
    context = {
    'fountain_locations': all_locations["Fountains"],
    'bus_stop_locations': all_locations["Bus stops"],
    'bin_locations': all_locations["Bins"],
    'maze': map,
    'theme_colour': [333, 589],
    'points': getattr(current_user_data, "score"),
    'item_list': item_list,
    'scores': leaderboard,
    'closest_things': loc_list,
    'location_form': LocationForm,
    'submitted': submitted,
    'streak': getattr(current_user_data, "streak"),
    'theme_colours': {'main':'#000000', 'second':'#7t12dd', 'icons':'#000000','background':'#000000'}
    } 
    return render(request, 'index.html', context)

def get_locations():
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
    
    all_locations = {"Fountains" : fountain_coordinates,
                     "Bus stops" : bus_stop_coordinates,
                     "Bins" : bin_coordinates}
    return all_locations

def get_leaderboard(length=5):
    leaderboard_list = UserProfile.objects.values().order_by("-score")
    leaderboard_list = leaderboard_list[:length]
    for profile in leaderboard_list:
        profile["username"] = User.objects.get(pk=profile["user_id"]).username
    return leaderboard_list