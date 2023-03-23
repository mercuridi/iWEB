# Dimitar: Imported the models so that the admin can access them
# Kai: Module docstring

"""
The admin module imports models so that the admin function of the side can access
them; ie. give the admin functionality to administrate
"""

from django.contrib import admin
from .models import Location, Item, UserProfile, Challenge, Usage

admin.site.register(Location)
admin.site.register(Item)
admin.site.register(UserProfile)
admin.site.register(Challenge)
admin.site.register(Usage)
