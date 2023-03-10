# Dimitar: Imported the models so that the admin can access them
# Kai: Wrote module docstring

"""Module imports models so that the admin function of the side can access
    them; ie. give the admin functionality to administrate
    """

from django.contrib import admin
from .models import Location
from .models import Item
from .models import UserProfile
from .models import Challenge

admin.site.register(Location)
admin.site.register(Item)
admin.site.register(UserProfile)
admin.site.register(Challenge)
