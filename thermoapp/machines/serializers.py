# django rest
from rest_framework import serializers

class MachineSerializer(serializers.Serializer):
    """Machine serializer"""
    id = serializers.CharField(max_length=25)
    Registered_by = serializers.CharField(max_length=55)
    Model = serializers.CharField(max_length=125)
    NEA_Classification = serializers.CharField(max_length=25)
    Serial = serializers.IntegerField()
    
    def validate(self, data):
        """Validates machine data"""
        
        #id = data['id']
        #if Machine.objects.get(id=id):
        #   raise serializers.ValidationError('This machine already exists')

        return data

