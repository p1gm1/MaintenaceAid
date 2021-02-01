from django.db import models
#from django.contrib.auth.models import User

#Model User
from thermoapp.users.models import User

#Model Machine
class Machine(models.Model):
	#public_id =CharField(max_length=255,primary_key=True, unique=True)
	register_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True) 
	model = models.CharField(max_length=255, blank=True, null=True)
	NEA_classification = models.CharField(max_length=255, blank=True, null=True)
	serial_number = models.CharField(max_length=512, blank=True, null=True)

	def __str__(self):
		return'{}'.format(self.id)