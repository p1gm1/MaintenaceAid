#Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _ 

class MachinesConfig(AppConfig):
    """Report app config"""
    name = "thermoapp.machines"
    verbose_name = _("Machines")