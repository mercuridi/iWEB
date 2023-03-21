"""
Python file representing the view for the main page most everything is contained in.
"""
import json
import random
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Location, Item, UserProfile
from .forms import LocationForm
from .utils.mapUtilities import read_map

def main(request):
    """
    This is the main page - everything but the login/register
    screen is contained in this file.
    """
    # load user info from request
    current_user = request.user
    current_user_data = UserProfile.objects.get(user = current_user)

    #post request handling
    submitted = False
    if request.method == "POST":
        data = json.loads(request.body)
        
        # leaderboard reset button handling
        if data.get("leaderboard_reset") == 0:
            all_profiles = UserProfile.objects.all()
            all_profiles.update(points_this_week=0,
                                challenge_done=False)
            for profile in all_profiles:
                profile.current_challenge_id = random.randint(1,3)
                profile.save
            
        # points handling
        points_change = data.get("points")
        if points_change is not None:
            if points_change > 0:
                # if we want to give the user points, it should be added to all 3 attributes
                current_user_data.points_lifetime   += points_change
                current_user_data.points_this_week  += points_change
                current_user_data.points_wallet     += points_change
            else:
                # if we want to take away points, they should only be taken from the wallet
                # eg. buying a theme uses this logic
                current_user_data.points_wallet     += points_change

        #theme purchase handling
        purchase = data.get("bought")
        if purchase is not None:
            current_user_data.owned_templates += " " + purchase

        # theme handling
        new_theme = data.get("newtheme")
        if new_theme is not None:
            current_user_data.current_template = new_theme

        # we've finished messing with the user profile now, so we save it to database
        current_user_data.save()

        #location request handling
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/addLocation?submitted=True')
    else:
        form = LocationForm
        if 'submitted' in request.GET:
            submitted = True

    # context setup
    # get location data from database   
    all_locations = get_locations()
    fountain_coordinates = all_locations["Fountains"]
    bus_stop_coordinates = all_locations["Bus stops"]
    bin_coordinates = all_locations["Bins"]
    leaderboard_list = get_leaderboard()
    map = read_map()
    
    # TODO need to write the function for loc_list to have them actually be closest.
    loc_list = Location.objects.values()

    #remove owned themes from shop
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

    # get the themes the user owns into the format the front end wants for settings
    all_themes = list(themes.keys())
    owned_themes = current_user_data.owned_templates
    for i in range(len(themes)):
        if all_themes[i] not in owned_themes:
            themes.pop(all_themes[i])

    context = {
    # map-related context
    'fountain_locations' : fountain_coordinates,
    'bus_stop_locations' : bus_stop_coordinates,
         'bin_locations' : bin_coordinates,
                  'maze' : map,
    # user-related data
          'display_name' : current_user_data.user,
                'streak' : current_user_data.streak,
         'points_wallet' : getattr(current_user_data, "points_wallet"),
           'points_week' : getattr(current_user_data, "points_this_week"),
       'points_lifetime' : getattr(current_user_data, "points_lifetime"),
              'is_staff' : getattr(current_user, "is_staff"),
    # site utilities
             'shop_list' : unowned_themes,
                'scores' : leaderboard_list,
        'closest_things' : loc_list,
         'location_form' : LocationForm,
             'submitted' : submitted,
    # settings data
                'themes' : themes,
                'colour' : themes[current_user_data.current_template],
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
        fountain_coordinates.append ([fountain.latitude, fountain.longitude, fountain.building, fountain.information])
    for bus_stop in bus_stop_locations:
        bus_stop_coordinates.append ([bus_stop.latitude, bus_stop.longitude, bus_stop.building, bus_stop.information])
    for bin in bin_locations:
        bin_coordinates.append      ([     bin.latitude,      bin.longitude,      bin.building,      bin.information])
    
    all_locations = {"Fountains" : fountain_coordinates,
                     "Bus stops" : bus_stop_coordinates,
                     "Bins" : bin_coordinates}
    return all_locations

def get_leaderboard(length=5):
    length = abs(length)    # just in case somehow we are asked for a negative number
    # get all the user profiles, ordered by the points they've got this week
    leaderboard_list = UserProfile.objects.values().order_by("-points_this_week")
    # remove staff accounts from the leaderboard
    for profile in leaderboard_list:
        if User.objects.get(pk=profile["user_id"]).is_staff is True:
            leaderboard_list = leaderboard_list.exclude(id=profile["user_id"])
    # slice the list to the requested length
    leaderboard_list = leaderboard_list[:length]
    # add username information to the profiles to be displayed
    for profile in leaderboard_list:
        profile["username"] = User.objects.get(pk=profile["user_id"]).username
    return leaderboard_list