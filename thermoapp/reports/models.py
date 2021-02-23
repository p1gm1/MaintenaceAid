from django.db import models
#from django.contrib.auth.models import User

#Models
from thermoapp.users.models import User
from thermoapp.machines.models import Machine


#Model Component
class Component(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	machine = models.ForeignKey(Machine, on_delete=models.CASCADE, blank=True, null=True)
	created = models.DateField(auto_now_add=True)
	component = models.CharField(max_length=255)
	detail = models.CharField(max_length=255)
	action = models.CharField(max_length=255, blank=True, null=True)
	is_active = models.BooleanField(default=True)
	t_max = models.FloatField(default=0.0,null=True,blank=True)
	t_min =models.FloatField(default=0.0,null=True,blank=True)

	def __str__(self):
		return'{}'.format(self.id)

#Model BasePhoto
class BasePhoto(models.Model):
	is_valid = models.BooleanField(default=True)
	is_active = models.BooleanField(default=True)
	picture = models.ImageField(upload_to='reports/pictures', 
								blank=True, 
								null=True)

	class Meta:
		"""Meta options."""
		abstract = True

#Model ThermoPhoto
class ThermoPhoto(BasePhoto):
	report = models.ForeignKey(Component, on_delete=models.CASCADE, blank=True, null=True)
	R1TMax = models.FloatField(blank=True, null=True)
	R1TMin = models.FloatField(blank=True, null=True)
	R1TMean = models.FloatField(blank=True, null=True)
	R2TMax = models.FloatField(blank=True, null=True)
	R2TMin = models.FloatField(blank=True, null=True)
	R2TMean = models.FloatField(blank=True, null=True)

	def __str__(self):
		return'{}-{}'.format(self.base.report.id,self.base.id)

#Model ContentPhoto
class ContentPhoto(BasePhoto):
	report = models.ForeignKey(Component, on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return'{}-{}'.format(self.base.report.id,self.base.id)
