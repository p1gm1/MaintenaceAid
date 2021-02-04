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

    def save(self, request):
        """Save method"""

        clean_sap = Machine.objects.filter(sap_code=self.cleaned_data['sap_code']).exists()

        if clean_sap:
            raise forms.ValidationError('Esta maquina ya existe.')
        else:
            data = self.cleaned_data

            data['register_by'] = User.objects.get(username=request.user.username)

            machine = Machine.objects.create(**data)
            machine.save()

            