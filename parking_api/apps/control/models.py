from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=255)
    cellphone = models.CharField(max_length=12, unique=True)

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")
        db_table = "clients"

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    type = models.CharField(max_length=255)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='vehicles')
    plate = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(
                regex=r'^[A-Z]{3}\d{1}[A-Z]{1}\d{2}$',
                message="Enter a valid MERCOSUL plate.",
                code="invalid_registration",
            ),
        ])

    class Meta:
        verbose_name = _("Vehicle")
        verbose_name_plural = _("Vehicles")
        db_table = "vehicles"

    def __str__(self):
        return self.plate
