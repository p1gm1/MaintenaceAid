# Django
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView, UpdateView

# Models
from thermoapp.machines.models import Machine

# Forms
from thermoapp.machines.forms import MachineCreateForm

# Django Rest
from rest_framework import (status, 
                            generics)

from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

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


class MachineUpdateView(LoginRequiredMixin, UpdateView):
    """Update machine info view."""
    template_name = 'machines/update.html'
    model = Machine 
    fields = ['serial_number', 'neta_classification', 'model', 'sap_code']

    def get_object(self):
        """Return machine model"""
        machine = Machine.objects.get(register_by=self.request.user)
        return machine

    def get_success_url(self):
        """Return to machines detail"""
        return reverse('machines:list_machines')


machine_update_view = MachineUpdateView.as_view()

    

      