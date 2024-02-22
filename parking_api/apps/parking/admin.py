from django.contrib import admin

from apps.parking.models import Parking, ParkingLot


@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ('id', 'parking_lot', 'vehicle', 'status')
    search_fields = ('id', 'parking_lot', 'vehicle', 'status')


@admin.register(ParkingLot)
class ParkingLotAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
