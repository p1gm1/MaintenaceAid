# Django
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, FormView 
from django.views.generic.list import ListView

# Models
from thermoapp.reports.models import Component
from thermoapp.machines.models import Machine

# Forms
from thermoapp.reports.forms import AddTermographyForm


class ComponentCreateView(LoginRequiredMixin, CreateView):
    """Machine component create
    view.
    """
    template_name='reports/create_component.html'
    model=Component
    fields = ['machine','component', 'detail', 'action', 't_max', 't_min']


    def form_valid(self, form):
        
        form.instance.user = self.request.user
        form.instance.machine.report_number += 1
        form.instance.machine.save()
        
        form.save()
        return super(ComponentCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("machines:list_machines")

create_report_view = ComponentCreateView.as_view()


class ComponentListView(LoginRequiredMixin, ListView):
    """Component list view."""

    model=Component
    template_name="reports/list_component.html"
    
    def get_queryset(self):
        queryset = Component.objects.filter(user=self.request.user,
                                            machine=Machine.objects.get(tag_model=self.kwargs['tag_model']))
        return queryset

list_report_view = ComponentListView.as_view()


class AddTermographyView(LoginRequiredMixin, FormView):
    """Add termography and content photo."""
    
    form_class = AddTermographyForm
    template_name = "reports/add_termography.html"
    pk = None

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            self.pk = kwargs['pk']
        if request.method == 'POST':
            kwargs.update({'pk': self.pk})
        print(kwargs)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save(self.kwargs)
        return super().form_valid(form)

    def get_success_url(self):
        tag_model = Component.objects.get(pk=self.kwargs['pk']).machine.tag_model
        return reverse("reports:list_component", kwargs={'tag_model': tag_model})

add_termography_view = AddTermographyView.as_view()