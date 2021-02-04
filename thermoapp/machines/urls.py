# Django
from django.urls import path

# Views
from thermoapp.machines.views import (machine_detail_view, 
                                      machine_create_view,
                                      machine_update_view)


urlpatterns = [
    path('list_machines/', view=machine_detail_view, name="list_machines"),
    path('create_machine/', view=machine_create_view, name="create_machine"),
    path('update_machine/', view=machine_update_view, name="update_machine"),
]