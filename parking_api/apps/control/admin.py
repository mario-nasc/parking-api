from django.contrib import admin

from apps.control.models import Client, Vehicle


class VehicleAdmin(admin.StackedInline):
    model = Vehicle
    extra = 1

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    inlines = (VehicleAdmin,)
    list_display = ('id', 'name', 'cellphone')
    search_fields = ('id', 'name', 'cellphone')
