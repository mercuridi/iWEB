# Dimitar: Imported the models so that the admin can access them

from django.contrib import admin
from .models import Location

admin.site.register(Location)
