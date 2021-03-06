from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db.models.fields import EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for thermoapp."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Nombre de usuario"), blank=True, max_length=255)

    def __str__(self):
        return '{}'.format(self.name)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
