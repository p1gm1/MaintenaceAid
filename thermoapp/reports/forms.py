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

# utils
from thermoapp.reports.utils import excel_to_dict

class TemperatureAndOcrThread(threading.Thread):
    """New thread that reads
    thermograp and adds to 
    report summary.
    """
    def __init__(self, thermo_photo, lock, *args, **kwargs):
        self.thermo_photo = thermo_photo
        self.lock = lock
        super(TemperatureAndOcrThread, self).__init__(*args, **kwargs)

    def run(self):
        
        self.lock.acquire(True)
        temp_and_ocr(self.thermo_photo)
        self.lock.release()


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
        
        lock = threading.Lock()
        TemperatureAndOcrThread(thermo_photo, lock).start()


class AddVibrationsExcelForm(forms.Form):
    """Vibrations Excel form class."""
    excel_file = forms.FileField(label='Archivo de Excel',
                                 widget=forms.FileInput(attrs={'class': 'form-control',
                                                               'required': True}))
    def save(self, pk):
        """Save method"""
        report = Component.objects.get(pk=pk)
        excel_dict = excel_to_dict(self.cleaned_data['excel_file'])

        for d in excel_dict:
            vibrations = Vibrations.objects.create(monitoring_point=d['monitoring_point'],
                                                   velocity=d['velocity'],
                                                   acelaration=d['aceleration'],
                                                   demod_spectrum=d['dem_odulada'],
                                                   report=report)
            vibrations.save()


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

