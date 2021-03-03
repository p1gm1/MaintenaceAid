# pytest
import pytest
import unittest

# Models
from thermoapp.reports.tests.factories import PhotoFactory

pytestmark = pytest.mark.django_db

def test_image_attribute():
    photo = PhotoFactory()
    
    assertions = unittest.TestCase('__init__')

    photo.content_picture.url = '/media/something/'

    assertions.assertNotEqual(photo.content_picture.url.split('/')[1], 'media')