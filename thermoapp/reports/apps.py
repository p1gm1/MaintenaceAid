#Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _ 

class ReportsConfig(AppConfig):
    """Report app config"""
    name = "thermoapp.reports"
    verbose_name = _("Reports")

    def ready(self):
        try:
            import reports.users.signals  # noqa F401
        except ImportError:
            pass