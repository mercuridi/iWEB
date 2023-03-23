# Beth: Accounts & login system
# Kai: Commenting & docstrings
"""
Module to define the login and accounts system.
Returns:
    Render requests for the server to handle when a user logs in or registers.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile
from .forms import NewUserForm

def register_request(request):
    """View to create a new user on the registration page"""
    if request.method == "POST":
        # create the form object
        form = NewUserForm(request.POST)
        
        # create the user and their profile if the registration is successful
        if form.is_valid():
            new_user = form.save()
            profile = UserProfile(user=new_user)
            profile.save()
            # automatically log in the new user
            login(request, new_user)
            messages.success(request, 'Registration successful.' )
            # redirect to main page
            return redirect('index')
        # if data is not valid, tell the user
        messages.error(request, 'Unsuccessful registration. Invalid information.')
    
    # create a fresh form object each time the page is rendered
    form = NewUserForm()
    # send the request to render the page
    return render(request=request, template_name='register.html', context={'register_form':form})
    
def login_request(request):
    """View to draw a login screen for users with existing accounts to use"""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # check the user actually exists
            user = authenticate(username=username, password=password)
            if user is not None:
                # if the username & password exist and match,
                # log the user in and redirect to main page
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('index')
            messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    # create a fresh form each time the page is rendered
    form = AuthenticationForm()
    # send the request to render the page
    return render(request=request, template_name="login.html", context={"login_form":form})
