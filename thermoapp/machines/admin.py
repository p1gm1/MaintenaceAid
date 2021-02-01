from django.contrib import admin

from thermoapp.machines.models import Machine

#This register allows to see the models in Django DB admin
admin.site.register(Machine)
