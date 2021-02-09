# django rest
from rest_framework import serializers

# Models
from thermoapp.users.models import User
from thermoapp.machines.models import Machine, SAPCode


class MachineModelSerializer(serializers.ModelSerializer):
    """Machine serializer"""
    class Meta:
        """Machine Meta Class."""
        model = Machine

        fields = '__all__'

                  
class CreateMachineSerializer(serializers.ModelSerializer):
    """Create machine serializer."""
    
    class Meta:
        model = Machine

        fields = ('model', 
                 'neta_classification', 
                 'serial_number',
                 'sap_code')

    def validate(self, data):
        """Validates machine data"""
        
        serial = data['serial']
        
        if Machine.objects.filter(serial_number=serial).exists():
            raise serializers.ValidationError('Esta maquina ya existe')
        
        return data

    def create(self, data):
        """Creates machine in the
        ORM
        """

        data['register_by'] = self.context['user']

        machine = Machine.objects.create(**data)
        SAPCode.objects.create(sap_code=data['sap_code'])

        return machine

