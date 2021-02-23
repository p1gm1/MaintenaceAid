# Django
from django.urls import path

# Views
from thermoapp.reports.views import create_report_view

urlpatterns = [
    path('create_report/', view=create_report_view, name="create_report")
]