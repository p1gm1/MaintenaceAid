from django.contrib import admin

from thermoapp.reports.models import Component, BasePhoto

#This register allows to see the models in Django DB admin
admin.site.register(Component)
admin.site.register(BasePhoto)