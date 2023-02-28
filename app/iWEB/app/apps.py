# Kai: Does anyone know what this does? Pylint doesn't like us redefining AppConfig after importing it. Why do we do this?

from django.apps import AppConfig

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
