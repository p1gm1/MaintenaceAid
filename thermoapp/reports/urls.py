# Django
from django.urls import path, include

#Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from thermoapp.reports.views import ReportViewSet

#View functions
from thermoapp.reports.views import *

router = DefaultRouter()
router.register(r'reports', ReportViewSet, basename='reports')

urlpatterns = [
    path('', include(router.urls)),
    # path('new_report', new_report, name=new_report),
]
