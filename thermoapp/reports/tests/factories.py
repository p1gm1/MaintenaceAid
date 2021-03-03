# Factory
from faker import Faker
from factory.django import DjangoModelFactory

# Django
from thermoapp.reports.models import BasePhoto

class PhotoFactory(DjangoModelFactory):
    """Base photo model
    factory"""

    content_picture = Faker().file_name(category='image', extension='jpg')
    thermo_picture = Faker().file_name(category='image', extension='jpg')

    class Meta:
        model=BasePhoto