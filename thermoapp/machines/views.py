#Django
from django.shortcuts import get_object_or_404

#Django Rest
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

# Serializers
from thermoapp.machines.serializers import MachineSerializer

# Permissions
from rest_framework.permissions import AllowAny


class MachineViewSet(viewsets.GenericViewSet,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,):
                    #  mixins.ListModelMixin,
                    #  mixins.CreateModelMixin
    """Machine view set.
    
    Handles machine detail and creation.
    """

    renderer_classes = [TemplateHTMLRenderer]

    def get_permissions(self):
        """Assign permissions based on action"""

        if self.action in ['list_machines', 'create_machine']:
            permissions = [AllowAny] #IsAuthenticated
        else:
            permissions = [AllowAny] #IsAdminUser

        return [p() for p in permissions]

    @action(detail=False, methods=['get'])
    def list_machines(self, request):
        # machines = Machine.objects.all()
        # self.object = machines
        # return Response({'machines: self.object'}, status=status.HTTP_200_OK, template_name='machines/detail.html')
        data = {'id': 'GENX-1', 
                'Registered_by': 'Pepito Perez',
                'Model': 'EX-T14R',
                'NEA_Classification': 'High',
                'Serial': 12568934}

        self.object = data
        
        return Response({'machines': self.object}, status=status.HTTP_200_OK, template_name='machines/detail.html')

    @action(detail=False, methods=['get','post'])
    def create_machine(self, request):
        serializer = MachineSerializer(data=request.data)
        
        if serializer.is_valid():
        #   serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.data, status=status.HTTP_200_OK, template_name='machines/create.html')
        

    def retrieve(self, request, pk=None):
        #queryset = Machine.objects.all()
        #machine = get_object_or_404(queryset, pk=pk)
        #serializer = MachineSerializer(machine)
        #return Response(serializer.data)
        pass

    def update(self, request, pk=None):
        #machine = Machine.object.get(pk=pk)
        #serializer = MachineSerializer(machine, data=request.data)
        #if serializer.is_valid():
        #   serializer.save()
        #   return Response(serializer.data)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        pass


      