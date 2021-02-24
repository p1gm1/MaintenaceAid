# Django
from django import forms

# Models
from thermoapp.reports.models import ContentPhoto, ThermoPhoto, Component

# Threads
import threading

# Object detection and ocr
from thermoapp.reports.object_detection import temp_and_ocr

class TemperatureAndOcrThread(threading.Thread):
    """New thread that reads
    thermograp and adds to 
    report summary.
    """
    def __init__(self, thermo_photo, *args, **kwargs):
        self.thermo_photo = thermo_photo
        super(TemperatureAndOcrThread, self).__init__(*args, **kwargs)

    def run(self):
        temp_and_ocr(self.thermo_photo)



class AddTermographyForm(forms.Form):
    """Termography and Content 
    form class"""

    thermo_photo = forms.ImageField(label='Foto Termografica',
                                    widget=forms.FileInput(attrs={'class': 'form-control',
                                                                  'required': True}))
    content_photo = forms.ImageField(label='Foto de contenido',
                                    widget=forms.FileInput(attrs={'class': 'form-control',
                                                                  'required': True}))
    
    def save(self, **kwargs):
        """Save method"""
        content_photo = ContentPhoto.objects.create(picture=self.cleaned_data['content_photo'],
                                                    is_valid=True,
                                                    report=Component.objects.get(pk=kwargs['pk']))
        content_photo.save()
        thermo_photo = ThermoPhoto.objects.create(picture=self.cleaned_data['thermo_photo'],
                                                  report=Component.objects.get(pk=kwargs['pk']))
        thermo_photo.save()

        TemperatureAndOcrThread(thermo_photo).start()

