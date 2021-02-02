# Django
from django.urls import path, include

#Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from thermoapp.machines.views import MachineViewSet

router = DefaultRouter()
router.register(r'machines', MachineViewSet, basename='machines')

urlpatterns = [
    path('', include(router.urls))
]