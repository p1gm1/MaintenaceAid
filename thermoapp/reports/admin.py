from django.contrib import admin

from thermoapp.reports.models import Component, ThermoPhoto, ContentPhoto

#This register allows to see the models in Django DB admin
admin.site.register(Component)
admin.site.register(ThermoPhoto)
admin.site.register(ContentPhoto)