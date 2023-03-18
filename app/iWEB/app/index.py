from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Location, Item, UserProfile
from .forms import LocationForm
from .utils.mapUtilities import read_map
import json

def main(request):
    """This is the main page - everything but the login/register screen should be in this view going forward"""
    # add location
    # load user info from request
    current_user = request.user
    current_user_data = UserProfile.objects.get(user = current_user)
    
    #post request handling
    submitted = False
    if request.method == "POST":
        data = json.loads(request.body)

        # points handling
        points = data.get("points")
        if points is not None:
            current_user_data.score += points
        
        #theme purchase handling
        purchase = data.get("bought")
        if purchase is not None:
            current_user_data.owned_templates += " " + purchase 

        # theme handling
        new_theme = data.get("newtheme")
        if new_theme is not None:
            current_user_data.current_template = new_theme
        else:
            current_user_data.current_template = "default"

        #location request handling
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/addLocation?submitted=True') #This should probably be changed to avoid redirects to a dead page

        current_user_data.save()
    else:
        form = LocationForm
        if 'submitted' in request.GET:
            submitted = True
    
    # context setup
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

    leaderboard_list = UserProfile.objects.values().order_by("-score")
    leaderboard_list = leaderboard_list[:5]
    for profile in leaderboard_list:
        profile["username"] = User.objects.get(pk=profile["user_id"]).username
            
    loc_list = Location.objects.values()
    
    #remove owned items from shop
    all_items = Item.objects.all()
    unowned_themes = []
    for item in all_items:
        if item.name not in current_user_data.owned_templates:
            unowned_themes.append(item)


    themes = {
        'default':  {'main':'#3776ac', 'second':'#7a12dd', 'icons':'#3776ac', 'background':'#ffffff','font':'#ffffff'},
        'first':    {'main':'#ffcccc', 'second':'#993366', 'icons':'#ff9999', 'background':'#ffdddd','font':'#aa0000'},
        'second':   {'main':'#ffcc66', 'second':'#ff6600', 'icons':'#ff9900', 'background':'#ffdd88','font':'#ffffff'},
        'third':    {'main':'#99ccff', 'second':'#6699cc', 'icons':'#6656ff', 'background':'#aaddff','font':'#444488'},
        'fourth':   {'main':'#ccff99', 'second':'#66cc99', 'icons':'#66cc99', 'background':'#ddffbb','font':'#054405'},
        'fifth':    {'main':'#ffcc99', 'second':'#cc6800', 'icons':'#cc6800', 'background':'#ffddbb','font':'#a20100'},
    }

    total_themes = ['default','first','second','third','fourth','fifth']
    owned_themes = current_user_data.owned_templates
    for i in range(len(themes)):
        if total_themes[i] not in owned_themes:
            themes.pop(total_themes[i])
    
    context = {
    'fountain_locations': fountain_coordinates,
    'bus_stop_locations': bus_stop_coordinates,
    'bin_locations': bin_coordinates,
    'maze': map,
    'points': getattr(current_user_data, "score"),
    'item_list': unowned_themes,
    'scores': leaderboard_list,
    'closest_things': loc_list,
    'location_form': LocationForm,
    'submitted': submitted,
    'streak':current_user_data.streak, #get streak of current user
    'themes': themes,
    'colour': themes[current_user_data.current_template],
    }

    return render(request, 'index.html', context)