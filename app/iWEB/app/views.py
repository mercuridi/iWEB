#Dimitar: home view, addLocation view

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Location, Item, pointsSystem
from .forms import LocationForm, NewUserForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

# Create your views here.
def index(request):
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

    return render(request, 'index.html',{'points': 256, 'item_list':itemList, 'scores':userList, 'closest_things': locList,'location_form': LocationForm, 'submitted': submitted})

def home(request):
    """View to pull data for the home screen"""
    all_items = Item.objects.all
    all_locations = Location.objects.all
    return render(request, 'home.html', {'all_items': all_items, 'all_locations': all_locations})

def register_request(request):
    """View to create a new user on the registration page"""
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            points = pointsSystem(streak=0, score=0, user=user)
            points.save()
            login(request, user)
            messages.success(request, 'Registration successful.' )
            return redirect('index')
        messages.error(request, 'Unsuccessful registration. Invalid information.')
    form = NewUserForm()
    return render(request=request, template_name='register.html', context={'register_form':form})
    
def login_request(request):
    """View to draw a login screen for users with existing accounts"""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('index')
            messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})
