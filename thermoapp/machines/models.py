# django
from django.db import models
#from django.contrib.auth.models import User

# Model
from thermoapp.users.models import User
from thermoapp.reports.models import SAPCode


#Model Machine
class Machine(models.Model):
	
	register_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True) 
	model = models.CharField(max_length=255, blank=True, null=True)
	neta_classification = models.CharField(max_length=255, blank=True, null=True)
	serial_number = models.CharField(max_length=51, blank=True, null=True, unique=True)
	report_number = models.IntegerField(default=0)
	sap_code = models.ForeignKey(SAPCode, on_delete=models.CASCADE, blank=True, null=True)
	location = models.CharField(max_length=55, blank=True, null=True)
	machine_type = models.CharField(max_length=55, blank=True, null=True)

	def __str__(self):
		return'{}'.format(self.serial_number)