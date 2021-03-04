# Django
from django.urls import path

# Views
from thermoapp.reports.views import (
    create_component_view,
    list_component_view,
    add_termography_view,
    report_view,
    update_termophoto_view,
    add_vibrations_view,
    )

urlpatterns = [
    path('<tag_model>/create_component/', view=create_component_view, name="create_component"),
    path('<tag_model>/list_component/', view=list_component_view, name="list_component"),
    path('<pk>/add_termography/', view=add_termography_view, name="add_termography"),
    path('<pk>/update_termography/', view=update_termophoto_view, name="update_thermophoto"),
    path('<tag_model>/report/', view=report_view, name="create_report"),
    path('<pk>/add_vibrations/', view=add_vibrations_view, name="add_vibration"),
]