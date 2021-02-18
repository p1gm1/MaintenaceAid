# Django
from django import forms

# Models
from thermoapp.users.models import User
from thermoapp.machines.models import Machine
from thermoapp.reports.models import Report


class MachineCreateForm(forms.Form):
    """Machine form class."""
    sap_code = forms.CharField(label='Codigo SAP',
                               max_length=55,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'required': True}))
    model = forms.CharField(label='Modelo',
                                    max_length=125,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'required': False}))
    neta_classification = forms.CharField(label='Clasificacion NETA',
                                         max_length=25,
                                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'required': True}))
    serial_number = forms.CharField(label='Serial',
                                    max_length=125,
                                    widget=forms.TextInput(attrs={'class':'form-control',
                                                           'required':False}))
    location = forms.CharField(label='Ubicacion',
                                max_length=55,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'required': False}))
    machine_type = forms.CharField(label='Tipo de maquina',
                                    max_length=55,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'required': True}))
    tag_model = forms.CharField(label='Tag de maquina',
                                    max_length=55,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'required': True}))

    def save(self, request):
        """Save method""" 

        if Machine.objects.filter(tag_model=self.cleaned_data['tag_model']).exists():
            raise forms.ValidationError('Esta maquina ya existe.')
        else:
            data = self.cleaned_data

            data['register_by'] = User.objects.get(username=request.user.username)

            machine = Machine.objects.create(**data)
            machine.save()

class ReportCreateForm(forms.Form):
    """Report form class."""
    component = forms.CharField(label='Componente',
                                max_length=55,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'required': True}))
    detail = forms.CharField(label='Detalle',
                             max_length=55,
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'required': False}))
    action = forms.CharField(label='Analisis y recomendaciones',
                             max_length=255,
                             widget=forms.Textarea({'class': 'form-control',
                                                    'required': False}))
    t_max = forms.FloatField(label='Temperatura maxima',
                             min_value=0.0,
                             widget=forms.NumberInput(attrs={'class': 'form-control',
                                                             'required': True}))
    t_min = forms.FloatField(label='Temperatura minima',
                             min_value=0.0,
                             widget=forms.NumberInput(attrs={'class': 'form-control',
                                                             'required': True}))
    thermo_photo = forms.ImageField(label='Foto termica',
                                    allow_empty_file=False,
                                    widget=forms.FileInput(attrs={'class': 'form-control',
                                                                  'required': True}))
    content_photo = forms.ImageField(label='Foto contenido',
                                    allow_empty_file=False,
                                    widget=forms.FileInput(attrs={'class': 'form-control',
                                                                  'required': True}))
    def save(self, request):
        """Save method"""
        print(request)

        data = self.cleaned_data
        data['user'] = User.objects.get(username=request.user.username)
        data['machine'] = Machine.objects.get(tag_model=self.tag_model)

        thermo_photo = data.pop('thermo_photo')
        content_photo = data.pop('content_photo')

        report = Report.objects.create(**data)
        report.save()
