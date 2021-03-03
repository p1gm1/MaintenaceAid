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
							  max_length=255)
	action = models.CharField(_("Accion"),
							  max_length=255, 
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

	def __str__(self):
		return'{}'.format(self.id)

#Model BasePhoto
class BasePhoto(models.Model):
	is_valid = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	report = models.ForeignKey(Component, on_delete=models.CASCADE, blank=True, null=True)
	thermo_picture = models.ImageField(upload_to='reports/pictures/thermo_photo', 
									   blank=True, 
									   null=True)
	content_picture = models.ImageField(upload_to='reports/pictures/content_photo/', 
										blank=True, 
										null=True)
	RTMax = models.FloatField(blank=True, null=True)
	RTMin = models.FloatField(blank=True, null=True)
	RTMean = models.FloatField(blank=True, null=True)

	def __str__(self):
		return'{}-{}'.format(self.report.id,self.id)