# Django
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView 

# Models
from thermoapp.reports.models import Component


class ReportCreateView(LoginRequiredMixin, CreateView):
    """Machine report create
    view.
    """
    template_name='reports/create_report.html'
    model=Component
    fields = ['machine','component', 'detail', 'action', 't_max', 't_min']


    def form_valid(self, form):
        
        form.instance.user = self.request.user
        form.instance.machine.report_number += 1
        form.instance.machine.save()
        
        form.save()
        return super(ReportCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("machines:list_machines")

create_report_view = ReportCreateView.as_view()