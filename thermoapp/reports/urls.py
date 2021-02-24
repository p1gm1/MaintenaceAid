# Django
from django.urls import path

# Views
from thermoapp.reports.views import (
    create_report_view,
    list_report_view,
    add_termography_view
    )

urlpatterns = [
    path('create_component/', view=create_report_view, name="create_component"),
    path('<tag_model>/list_component/', view=list_report_view, name="list_component"),
    path('<pk>/add_termography/', view=add_termography_view, name="add_termography")
]