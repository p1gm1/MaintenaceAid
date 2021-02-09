# Django
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView

# Models
from thermoapp.machines.models import Machine
from thermoapp.reports.models import SAPCode

# Form
from thermoapp.machines.forms import MachineCreateForm

# # Serializers
# from thermoapp.machines.serializers import CreateMachineSerializer, MachineModelSerializer

# Django Rest
from rest_framework import (status, 
                            generics)

from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
#from rest_framework.parsers import MultiPartParser

# Permissions
from rest_framework.permissions import AllowAny


class MachineListView(generics.ListAPIView):
                   
    """Machine view set.
    
    Handles machine detail.
    """

    renderer_classes = [TemplateHTMLRenderer]

    def get_permissions(self):
        """Assign permissions based on action"""

        permissions = [AllowAny] #IsAuthenticated
        

        return [p() for p in permissions]

    def get(self, request):
        machines = Machine.objects.all()
        self.object = machines
        
        return Response(data={'machines': self.object}, status=status.HTTP_200_OK, template_name='machines/detail.html')


machine_detail_view = MachineListView.as_view()


# class MachineCreateView(generics.ListCreateAPIView):
#     """Create machine view."""
#     serializer_class = CreateMachineSerializer
#     renderer_classes = [TemplateHTMLRenderer]
#     #parser_classes = [MultiPartParser]

#     def get_permissions(self):
#         """Assign permissions based on action"""

#         permissions = [AllowAny] #IsAuthenticated
        
#         return [p() for p in permissions]

#     def get_serializer_context(self):
#         """Add user to serializer context"""
#         context = super(MachineCreateView, self).get_serializer_context()
#         context['user'] = self.request.user
        
#         return context

#     def get(self, request):
#         """Get form page."""
#         return Response(request.data, status=status.HTTP_200_OK, template_name='machines/create.html')

#     def post(self, request, *args, **kwargs):
#         """Form post action."""

#         serializer_class = self.get_serializer_class()

#         context = self.get_serializer_context()

#         serializer = serializer_class(data=request.data, context=context)
       
#         serializer.is_valid(raise_exception=True)

#         machine = serializer.save()

#         data = MachineModelSerializer(machine).data

#         return Response(data, status=status.HTTP_201_CREATED, template_name='machines/detail.html')

# machine_create_view = MachineCreateView.as_view()
class MachineCreateView(LoginRequiredMixin, FormView):
    """Machine create set.
    
    Handles machine creation.
    """
    model = Machine
    form_class = MachineCreateForm
    template_name="machines/create.html"

    def form_valid(self, form):
        form.save(self.request)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("machines:list_machines")
        

machine_create_view = MachineCreateView.as_view()

    

      