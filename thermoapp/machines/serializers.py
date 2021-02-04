# django rest
from rest_framework import serializers

# Models
from thermoapp.users.models import User
from thermoapp.machines.models import Machine
from thermoapp.reports.models import SAPCode

class MachineSerializer(serializers.Serializer):
    """Machine serializer"""
    SAP_code = serializers.CharField(max_length=55)
    machine_model = serializers.CharField(max_length=125)
    NEA_classification = serializers.CharField(max_length=25)
    serial = serializers.CharField(max_length=125)
    
    def validate(self, data):
        """Validates machine data"""
        
        sap = data[0]['SAP_code']
        
        try: 
            SAPCode.objects.get(sap_code=sap)
            raise serializers.ValidationError('This machine already exists')
        except:
            return data

    def create(self, data):
        """Creates machine in the
        ORM
        """

        data[0]['register_by'] = User.objects.get(username=data[1])

        machine = Machine.objects.create(**data[0])
        SAPCode.objects.create(
                        sap_code=data[0]['SAP_code'],
                        user = data[0]['register_by'],
                        machine = machine
        )

        return machine

