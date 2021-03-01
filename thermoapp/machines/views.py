# Django
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import  FormView, UpdateView
from django.views.generic.list import ListView

# Models
from thermoapp.machines.models import Machine

# Form
from thermoapp.machines.forms import MachineCreateForm


class MachineListView(LoginRequiredMixin, ListView):
    """Machine list view.
    """

    model = Machine
    template_name = "machines/detail.html"

    def get_queryset(self):
        queryset = Machine.objects.filter(register_by=self.request.user)
        return queryset

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