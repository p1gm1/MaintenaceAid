from django.db import models
#from django.contrib.auth.models import User

#Models
from thermoapp.users.models import User


#Model Report
class Report(models.Model):
	#public_id =CharField(max_length=255,primary_key=True, unique=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	created = models.DateField(auto_now_add=True)
	component = models.CharField(max_length=255)
	detail = models.CharField(max_length=255)
	action = models.CharField(max_length=255, blank=True, null=True)
	is_active = models.BooleanField(default=True)
	t_max = models.FloatField(null=True,blank=True)
	t_min =models.FloatField(null=True,blank=True)
	bucket_url = models.TextField()

	def __str__(self):
		return'{}'.format(self.id)

class SAPCode(models.Model):
	sap_code = models.CharField(max_length=55, primary_key=True, unique=True)
	report = models.ForeignKey(Report, on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return '{}'.format(self.sap_code)

#Model BasePhoto
class BasePhoto(models.Model):
	#public_id = CharField(max_length=255,primary_key=True, unique=True)
	report = models.ForeignKey(Report, on_delete=models.CASCADE, blank=True, null=True)
	is_valid = models.BooleanField(default=True)
	is_active = models.BooleanField(default=True)
	bucket_url = models.TextField()

#Model ThermoPhoto
class ThermoPhoto(models.Model):
	base = models.ForeignKey(BasePhoto, on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return'{}-{}'.format(self.base.report.id,self.base.id)

#Model ContentPhoto
class ContentPhoto(models.Model):
	base = models.ForeignKey(BasePhoto, on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return'{}-{}'.format(self.base.report.id,self.base.id)
