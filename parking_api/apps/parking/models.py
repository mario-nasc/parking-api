from django.utils.translation import gettext_lazy as _
from django.db import models

from apps.control.models import Vehicle


class ParkingLot(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("ParkingLot")
        verbose_name_plural = _("ParkingLots")
        db_table = "parking_lots"


class Parking(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name='parking', on_delete=models.CASCADE)
    parking_lot = models.ForeignKey(ParkingLot, related_name='parking', on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True)
    left_at = models.DateTimeField(null=True)

    class Meta:
        verbose_name = _("Parking")
        verbose_name_plural = _("Parkings")
        db_table = "parkings"
