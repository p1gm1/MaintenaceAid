# django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Model
from thermoapp.users.models import User


#Model Machine
class Machine(models.Model):
	
	register_by = models.ForeignKey(User, 
									on_delete=models.CASCADE,
									verbose_name=_("Registrado por"), 
									blank=True, 
									null=True) 
	picture = models.ImageField(_("Foto"),
								upload_to='machines/pictures',
								blank=True,
								null=True)
	model = models.CharField(_("Modelo"),
							 max_length=255, 
							 blank=True, 
							 null=True)
	neta_classification = models.CharField(_("Clasificacion NETA"),
										   max_length=255, 
										   blank=True, 
										   null=True)
	serial_number = models.CharField(_("Numero serial"),
									 max_length=51, 
									 blank=True, 
									 null=True, 
									 unique=True)
	report_number = models.IntegerField(default=0)
	sap_code = models.CharField(_("Codigo SAP"), 
								max_length=51,
								blank=True, 
								null=True)
	location = models.CharField(_("Ubicacion"),
								max_length=55, 
								blank=True, 
								null=True)
	machine_type = models.CharField(_("Tipo de maquina"),
									max_length=55, 
									blank=True, 
									null=True)
	tag_model = models.CharField(_("Modelo TAG"),
								 max_length=55, 
								 blank=True, 
								 null=True, 
								 unique=True)

	def __str__(self):
		return'{}'.format(self.tag_model)