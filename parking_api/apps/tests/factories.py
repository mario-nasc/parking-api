import factory

from apps.control.models import Client, Vehicle
from apps.parking.models import Parking


class VehicleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vehicle


class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Client


class ParkingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Parking
