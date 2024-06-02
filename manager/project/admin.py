from django.contrib import admin
from django.apps import apps
from project.models import *
app_models = apps.get_app_config('project').get_models()
admin.site.site_header = 'Paneli i Administratorit'

for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
