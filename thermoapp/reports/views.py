# Django
from django.forms.forms import Form
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, FormView, UpdateView 
from django.views.generic.list import ListView

# Models
from thermoapp.reports.models import Component, BasePhoto, Vibrations, Report
from thermoapp.machines.models import Machine

# Forms
from thermoapp.reports.forms import (AddTermographyForm, 
                                     TemperatureAndOcrThread,
                                     AddVibrationForm,
                                     AddVibrationsExcelForm)

# utils
from thermoapp.reports.utils import VibrationsPoints

class ComponentCreateView(LoginRequiredMixin, CreateView):
    """Machine component create
    view.
    """
    template_name='reports/create_component.html'
    model=Component
    fields = ['component', 
              'detail', 
              'action',
              'tag_model', 
              't_max', 
              't_min',
              'vel_max',
              'vel_min',
              'ace_max',
              'ace_min',
              'v_max',
              'v_min']
    queryset = Machine.objects.all()

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            self.tag_model = kwargs['tag_model']
            kwargs.update({'tag_model': self.tag_model})
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        self.extra_context = {'machine': self.queryset.get(tag_model=self.kwargs['tag_model'])}
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        
        form.instance.user = self.request.user
        form.instance.machine = self.get_context_data()['machine']
        form.instance.machine.report_number += 1
        form.instance.machine.save()

        form.save()
        return super(ComponentCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("machines:list_machines")

create_component_view = ComponentCreateView.as_view()


class ComponentListView(LoginRequiredMixin, ListView):
    """Component list view."""

    model=Component
    template_name="reports/list_component.html"
    
    def get_queryset(self):
        queryset = Component.objects.filter(user=self.request.user,
                                            machine=Machine.objects.get(tag_model=self.kwargs['tag_model']))
        return queryset

list_component_view = ComponentListView.as_view()


class ComponentUpdateView(LoginRequiredMixin, UpdateView):
    """Update component view."""
    template_name='reports/update_component.html'
    model=Component
    fields=('component', 'detail', 'action', 'tag_model')

    def get_queryset(self):
        return Component.objects.all()

    def get_success_url(self):
        tag_model=self.get_queryset().get(pk=self.kwargs['pk']).machine.tag_model
        return reverse("reports:list_component", kwargs={'tag_model': tag_model})

update_component_view = ComponentUpdateView.as_view()


class AddTermographyView(LoginRequiredMixin, FormView):
    """Add termography and content photo."""
    
    form_class = AddTermographyForm
    template_name = "reports/add_termography.html"
    queryset = Component.objects.all()

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            self.pk = kwargs['pk']
            kwargs.update({'pk': self.pk})
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        self.extra_context = {'instance': self.queryset.get(pk=self.kwargs['pk'])} 
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        pk = self.kwargs['pk']
        form.save(pk)
        return super().form_valid(form)

    def get_success_url(self):
        tag_model = Component.objects.get(pk=self.kwargs['pk']).machine.tag_model
        return reverse("reports:list_component", kwargs={'tag_model': tag_model})

add_termography_view = AddTermographyView.as_view()


class UpdateTermographyView(LoginRequiredMixin, UpdateView):
    """Update a termograph"""
    template_name='reports/update_termography.html'
    model = BasePhoto
    fields = ('thermo_picture', 'content_picture')

    def get_queryset(self):
        return BasePhoto.objects.all()

    def form_valid(self, form):
        form.save()
        TemperatureAndOcrThread(self.object).start()
        return super().form_valid(form)

    def get_success_url(self):
        tag_model = self.object.report.machine.tag_model
        return reverse('reports:list_component', kwargs={'tag_model': tag_model})

update_termophoto_view = UpdateTermographyView.as_view()


class AddVibrationsView(LoginRequiredMixin, FormView):
    """Add vibrations info"""

    form_class = AddVibrationForm
    template_name = "reports/add_vibrations.html"
    queryset = Component.objects.all()

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            self.pk = kwargs['pk']
            kwargs.update({'pk': self.pk})
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        self.extra_context = {'instance': self.queryset.get(pk=self.kwargs['pk'])}
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        pk = self.kwargs['pk']
        form.save(pk)
        return super().form_valid(form)

    def get_success_url(self):
        tag_model = Component.objects.get(pk=self.kwargs['pk']).machine.tag_model
        return reverse("reports:list_component", kwargs={'tag_model': tag_model})

add_vibrations_view = AddVibrationsView.as_view()


class AddVibrationsExcelView(LoginRequiredMixin, FormView):
    """Add vribrations excel"""

    form_class=AddVibrationsExcelForm
    template_name="reports/add_vibrations_excel.html"
    queryset = Component.objects.all()

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            self.pk = kwargs['pk']
            kwargs.update({'pk': self.pk})
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        self.extra_context = {'instance': self.queryset.get(pk=self.kwargs['pk'])}
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        pk = self.kwargs['pk']
        form.save(pk)
        return super().form_valid(form)

    def get_success_url(self):
        tag_model = Component.objects.get(pk=self.kwargs['pk']).machine.tag_model
        return reverse("reports:list_component", kwargs={'tag_model': tag_model})

add_vibrations_excel_view = AddVibrationsExcelView.as_view()


class ReportView(LoginRequiredMixin, ListView):
    """Make a report of the added, 
    thermography
    """

    model = Report
    template_name = "reports/create_report.html"
    queryset = Machine.objects.all()

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            self.tag_model = kwargs['tag_model']
            kwargs.update({'tag_model': self.tag_model})
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        q = Component.objects.filter(user=self.request.user,
                                     machine=Machine.objects.get(tag_model=self.kwargs['tag_model']))
        
        mp = ''
        vib_list=[]

        vibrations = [Vibrations.objects.filter(report=c) for c in q]
        
        for q in vibrations:
            for j in range(len(q)):
                arr_m = Vibrations.objects.filter(monitoring_point=q[j].monitoring_point)
                
                if mp != arr_m.first().monitoring_point:
                    mp = arr_m.first().monitoring_point
                    if (len(arr_m) > 2):
                        vib_obj = VibrationsPoints(
                            component=arr_m.first().report.component,
                            monitoring_point=mp,
                            created=arr_m.last().created,
                            vel_prev= arr_m.reverse()[len(arr_m)-2].velocity,
                            vel_last=arr_m.last().velocity,
                            ace_prev=arr_m.reverse()[len(arr_m)-2].acelaration,
                            ace_last=arr_m.last().acelaration,
                            dem_prev=arr_m.reverse()[len(arr_m)-2].demod_spectrum,
                            dem_last=arr_m.last().demod_spectrum
                            )
                        vib_obj.find_outliers()
                    else:
                        vib_obj = VibrationsPoints(
                            component=arr_m.first().report.component,
                            monitoring_point=mp,
                            created=arr_m.last().created,
                            vel_prev= arr_m.first().velocity,
                            vel_last=arr_m.last().velocity,
                            ace_prev=arr_m.first().acelaration,
                            ace_last=arr_m.last().acelaration,
                            dem_prev=arr_m.first().demod_spectrum,
                            dem_last=arr_m.last().demod_spectrum
                            )
                        vib_obj.find_outliers()
                    vib_list.append(vib_obj)
                    
                else:
                    continue
        
        self.extra_context = {
            'machine': self.queryset.get(tag_model=self.kwargs['tag_model']),
            'vibrations': vib_list,
            'components': Component.objects.filter(user=self.request.user,
                                     machine=Machine.objects.get(tag_model=self.kwargs['tag_model'])),
                              }
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        q = Component.objects.filter(user=self.request.user,
                                     machine=Machine.objects.get(tag_model=self.kwargs['tag_model']))
        
        queryset = [BasePhoto.objects.filter(report=c) for c in q]

        return queryset

report_view = ReportView.as_view()


