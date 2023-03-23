# Dimitar: Location form POST request handling
# Kai: Leaderboard reset, points, theme purchase, theme equipping, all 
#       context data passed to front end, get_leaderboard and get_locations functions,
#       commenting, docstrings, refactoring
# Dash: Colour codes for themes
# Jude: Colour tweaking for compatibility/readability, Theme handling before refactor,
#       organising of all code into single file after restructuring
"""
Python file representing the view for the main page most everything is contained in.
"""
import json
import random
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Location, Item, UserProfile, Challenge, Usage
from .forms import LocationForm
from .utils.mapUtilities import read_map

def main(request):
    """
    This is the main page - the backend for everything but
    the login/register/help screens are contained in this file.
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
            if current_user.is_staff:
                all_profiles = UserProfile.objects.all()
                # iterate across users to give them each a new random challenge
                # (new challenge can be the same as the last one)
                # also, if they haven't completed their challenge, reset their streak
                for profile in all_profiles:
                    UserProfile.objects.filter(id=profile.id).update(current_challenge_id=random.randint(1,3))
                    UserProfile.objects.filter(challenge_done=False).update(streak=0)
                # set all users at once to have 0 points this week and an incomplete challenge
                UserProfile.objects.all().update(
                    points_this_week=0,
                    challenge_done=False,
                    )
                
        # streak incrementation and handling upon challenge completion
        location_used = data.get("type_used")
        if location_used is not None:
            if current_user_data.current_challenge.type == location_used:
                if current_user_data.challenge_done is False:
                    # Set the challenge to done, increment streak
                    current_user_data.challenge_done = True
                    current_user_data.streak += 1
                    
                    # Bonus points for completing the challenge
                    bonus_points = 500
                    current_user_data.points_lifetime   += bonus_points
                    current_user_data.points_this_week  += bonus_points
                    current_user_data.points_wallet     += bonus_points
            
            usage = Usage.objects.get(pk=1)
            usage.total_used += 1
            match(location_used):
                case("fountain"):
                    usage.fountains_used += 1
                case("bus_stop"):
                    usage.bus_stops_used += 1
                case("bin"):
                    usage.bins_used += 1
            usage.save()
                    
            
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

        location_data = data.get("location")
        #location request handling
        if location_data:
            print("Location data received: " + str(location_data))
            form = LocationForm(location_data)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/addLocation?submitted=True')
            else:
                print("Form is not valid")
                # Handle form validation errors here
    else:
        form = LocationForm
        if 'submitted' in request.GET:
            submitted = True

    # context setup
    # get location data from database in front-end formatting  
    all_locations = get_locations()
    
    # get leaderboard from database in front-end formatting
    leaderboard_list = get_leaderboard()
    
    # get the list of lists representation of the map for front-end
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

    # handle total stats for display on main page         
    usage = Usage.objects.get(pk=1)
    fountains_used = usage.fountains_used * 54
    bus_stops_used = usage.bus_stops_used
    bins_used = usage.bins_used
    total_used = usage.total_used

    context = {
    # map-related context
    'fountain_locations' : all_locations["Fountains"],
    'bus_stop_locations' : all_locations["Bus stops"],
         'bin_locations' : all_locations["Bins"],
                  'maze' : map,
    # user-related data
          'display_name' : current_user_data.user,
         'points_wallet' : getattr(current_user_data, "points_wallet"),
           'points_week' : getattr(current_user_data, "points_this_week"),
       'points_lifetime' : getattr(current_user_data, "points_lifetime"),
     'current_challenge' : getattr(current_user_data, "current_challenge"),
        'challenge_done' : getattr(current_user_data, "challenge_done"),
              'is_staff' : getattr(current_user, "is_staff"),
                'streak' : current_user_data.streak,
    # site utilities
            'usage_data' : {'fountains_used':fountains_used,'bus_stops_used':bus_stops_used,'bins_used':bins_used,'total_used':total_used},
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
    """
    Method to get all the location data out of the database in a format the front-end likes.
    Returns:
        all_locations (dict) : A dictionary of locations, with their types as the key.
                                The values are lists of lists concerning each location's data, as used by the front-end.
    """
    # Get the different types of location
    fountain_locations = Location.objects.filter(type='Fountain')
    bus_stop_locations = Location.objects.filter(type='BusStop')
    bin_locations = Location.objects.filter(type='Bin')
    
    # Define some empty lists we're going to populate
    fountain_information = []
    bus_stop_information = []
    bin_information = []
    
    for fountain in fountain_locations:
        fountain_information.append ([fountain.latitude, fountain.longitude, fountain.building, fountain.information])
    for bus_stop in bus_stop_locations:
        bus_stop_information.append ([bus_stop.latitude, bus_stop.longitude, bus_stop.building, bus_stop.information])
    for bin in bin_locations:
        bin_information.append      ([     bin.latitude,      bin.longitude,      bin.building,      bin.information])
    
    all_locations = {"Fountains" : fountain_information,
                     "Bus stops" : bus_stop_information,
                     "Bins" : bin_information}
    return all_locations

def get_leaderboard(length=5):
    """
    Method to get the leaderboard from the database
    Args:
        length (int, optional): The length of the leaderboard you want. Defaults to 5.
        e.g. a large implementation of iWEB might want to show the top 100 users instead of the top 5.
    Returns:
        leaderboard_list (QuerySet) :   A query set of (length) users, 
                                        ordered by the most points earned this week.
    """
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
