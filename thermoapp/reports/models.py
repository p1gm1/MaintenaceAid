# django
from django.db import models
from django.utils.translation import gettext_lazy as _

#Models
from thermoapp.users.models import User
from thermoapp.machines.models import Machine


#Model Component
class Component(models.Model):
	user = models.ForeignKey(User, 
							 on_delete=models.CASCADE,
							 verbose_name=_("Creado por"), 
							 blank=True, null=True)
	machine = models.ForeignKey(Machine, 
								on_delete=models.CASCADE,
								verbose_name=_("Maquina"), 
								blank=True, 
								null=True)
	created = models.DateField(_("Fecha de registro"),auto_now_add=True)
	component = models.CharField(_("Componente"),max_length=255)
	detail = models.CharField(_("Detalle"),
							  max_length=255,
							  blank=True, 
							  null=True)
	action = models.CharField(_("Accion"),
							  max_length=255, 
							  blank=True, 
							  null=True)
	tag_model = models.CharField(_("Tag"),
								 max_length=55,
								 blank=True, 
							     null=True)
	is_active = models.BooleanField(default=True)
	t_max = models.FloatField(_("Temperatura máxima"),
							  default=0.0,
							  null=True,
							  blank=True)
	t_min =models.FloatField(_("Temperatura mínima"),
							 default=0.0,
							 null=True,
							 blank=True)
	v_max = models.FloatField(_("Vibracion máxima"),
							  default=0.0,
							  null=True,
							  blank=True)
	v_min = models.FloatField(_("Vibración mínima"),
							  default=0.0,
							  null=True,
							  blank=True)
	vel_max = models.FloatField(_("Velocidad máxima"),
							  default=0.0,
							  null=True,
							  blank=True)
	vel_min = models.FloatField(_("Velocidad mínima"),
							  default=0.0,
							  null=True,
							  blank=True)
	ace_max = models.FloatField(_("Aceleración máxima"),
							  default=0.0,
							  null=True,
							  blank=True)
	ace_min = models.FloatField(_("Aceleración mínima"),
							  default=0.0,
							  null=True,
							  blank=True)

	def __str__(self):
		return'{}'.format(self.tag_model)

#Model BasePhoto
class BasePhoto(models.Model):
	is_valid = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	report = models.ForeignKey(Component, on_delete=models.CASCADE, blank=True, null=True)
	thermo_picture = models.ImageField(_("Foto Termica"),
									   upload_to='reports/pictures/thermo_photo', 
									   blank=True, 
									   null=True)
	content_picture = models.ImageField(_("Foto de contenido"),
										upload_to='reports/pictures/content_photo/', 
										blank=True, 
										null=True)
	RTMax = models.FloatField(blank=True, null=True)
	RTMin = models.FloatField(blank=True, null=True)
	RTMean = models.FloatField(blank=True, null=True)

	def __str__(self):
		return'{}-{}'.format(self.report.tag_model,self.id)

#Model Vibrations
class Vibrations(models.Model):
	report = models.ForeignKey(Component, 
							   on_delete=models.CASCADE, 
							   blank=True, 
							   null=True)
	created = models.DateField(_("Fecha de registro"),auto_now_add=True)
	monitoring_point = models.CharField(_("Punto de monitoreo"),
									   max_length=150,  
									   blank=True, 
									   null=True)
	velocity = models.FloatField(_("Velocidad"), 
								 null=True, 
								 blank=True)
	acelaration = models.FloatField(_("Aceleracion"),
								    null=True, 
									blank=True)
	demod_spectrum = models.FloatField(_("Dem Odulada"), 
									   null=True, 
									   blank=True)

	def __str__(self):
		return'{}-{}'.format(self.report.tag_model, self.id)

#Model Report
class Report(models.Model):
	user = models.ForeignKey(User,
							 on_delete=models.CASCADE,
							 blank=True,
							 null=True)
	machine = models.ForeignKey(Machine,
								on_delete=models.CASCADE,
								blank=True,
								null=True)
	component = models.ForeignKey(Component,
								  on_delete=models.CASCADE,
								  blank=True,
								  null=True)