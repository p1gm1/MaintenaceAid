# Django
from django import forms

# Models
from thermoapp.users.models import User
from thermoapp.machines.models import Machine


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
    instalation_date = forms.DateField(label="Fecha de instalación",
                                       widget=forms.DateInput(attrs={'class': 'form-control',
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

