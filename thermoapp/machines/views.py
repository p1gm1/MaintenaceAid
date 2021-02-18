# Django
from thermoapp.reports.models import Report
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView

# Models
from thermoapp.machines.models import Machine
from thermoapp.reports.models import Report

# Form
from thermoapp.machines.forms import MachineCreateForm, ReportCreateForm

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
        machines = Machine.objects.filter(register_by=request.user)
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


class MachineDetailView(LoginRequiredMixin, DetailView):
    """Machine detail view."""
    model=Machine
    template_name = 'machines/inspect.html'
    slug_field = 'tag_model'
    slug_url_kwarg = 'tag_model'

machine_inspect_view = MachineDetailView.as_view()

class UpdateMachineView(LoginRequiredMixin, UpdateView):
    """Update machine view."""
    template_name = 'machines/update.html'
    slug_field = 'tag_model'
    slug_url_kwarg = 'tag_model'
    model = Machine
    fields = ('picture',
              'model', 
              'serial_number', 
              'sap_code', 
              'location', 
              'machine_type', 
              'tag_model')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        tag_model = self.object.tag_model
        return reverse('machines:detail_machine', kwargs={'tag_model': tag_model})

machine_update_view = UpdateMachineView.as_view()


class MachineReportCreateView(LoginRequiredMixin, CreateView):
    """Machine report create
    view.
    """
    template_name='machines/create_report.html'
    model=Report
    fields = ['component', 'detail', 'action', 't_max', 't_min']
    queryset = Machine.objects.all()
    
    def __init__(self):
        self.tag_model='PME-345'
        return super().__init__()

    def get(self, request, *args, **kwargs):
        """Modified version of
        get method to catch tag_model.
        """
        self.tag_model = kwargs.get('tag_model')
        return super().get(self, request, *args, **kwargs)

    def form_valid(self, form):
        
        machine = self.queryset.get(tag_model=str(self.tag_model))
        form.instance.user = self.request.user
        form.instance.machine = machine 
        machine.report_number += 1
        machine.save()
        form.save()
        return super(MachineReportCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("machines:list_machines")

machine_create_report_view = MachineReportCreateView.as_view()