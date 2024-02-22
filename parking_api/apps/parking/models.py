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

    @property
    def status(self):
        if self.left_at:
            return 'Carro saiu do estacionamento'
        if self.paid_at and not self.left_at:
            return 'Pendente pagamento'
        if not self.paid_at and not self.left_at:
            return "No estacionamento" 

    class Meta:
        verbose_name = _("Parking")
        verbose_name_plural = _("Parkings")
        db_table = "parkings"
