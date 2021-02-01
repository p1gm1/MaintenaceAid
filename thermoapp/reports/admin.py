from django.contrib import admin

from thermoapp.reports.models import Report, ThermoPhoto, ContentPhoto, SAPCode

#This register allows to see the models in Django DB admin
admin.site.register(Report)
admin.site.register(ThermoPhoto)
admin.site.register(ContentPhoto)
admin.site.register(SAPCode)