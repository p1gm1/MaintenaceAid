# Django
from django import forms

# Models
from thermoapp.reports.models import (BasePhoto, 
                                      Vibrations, 
                                      Component)

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
    
    def save(self, pk):
        """Save method"""
        thermo_photo = BasePhoto.objects.create(thermo_picture=self.cleaned_data['thermo_photo'],
                                                content_picture=self.cleaned_data['content_photo'],
                                                report=Component.objects.get(pk=pk))
        thermo_photo.save()
        

        TemperatureAndOcrThread(thermo_photo).start()


class AddVibrationForm(forms.Form):
    """Vibrations form class"""
    
    monitoring_point = forms.CharField(label='Punto de monitoreo',
                                       widget=forms.TextInput(attrs={'class': 'form-control',
                                                                     'required': True}))
    velocity = forms.FloatField(label='Velocidad',
                                widget=forms.NumberInput(attrs={'class': 'form-control',
                                                              'required': True}))
    acelaration = forms.FloatField(label='Aceleración',
                                  widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                'required': True}))
    demod_spectrum = forms.FloatField(label='Dem Odulada',
                                     widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                   'required': True}))
    
    def save(self, pk):
        """Save method"""
        vibrations = Vibrations.objects.create(monitoring_point=self.cleaned_data['monitoring_point'],
                                               velocity=self.cleaned_data['velocity'],
                                               acelaration=self.cleaned_data['acelaration'],
                                               demod_spectrum=self.cleaned_data['demod_spectrum'], 
                                               report=Component.objects.get(pk=pk))
        vibrations.save()

