"""
Define the names of the apps we use. Since all our work is in one app, we just call it "app".
"""
from django.apps import AppConfig
class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
