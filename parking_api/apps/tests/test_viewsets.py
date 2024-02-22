import os
import pytest
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.tests.factories import ClientFactory, ParkingFactory, VehicleFactory
from parking_api.settings import BASE_DIR
from datetime import datetime


@pytest.fixture(scope='session')
def django_db_setup(django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', os.path.join(BASE_DIR, 'initial_data.json'))


def _create_parking():
    client = ClientFactory(name='Mario', cellphone='85988889991')
    vehicle = VehicleFactory(type='gol', plate='POB3E70', client=client)
    return ParkingFactory(vehicle=vehicle, started_at=datetime.utcnow(), parking_lot_id=1)


class EnterParkingTestCase(APITestCase):

    
    def setUp(self):
        self.url = reverse("parking:enter_parking", kwargs={'parking_lot_id': 1})
        self.data = {
            "client": {
                "cellphone": "85988889991",
                "name": "Mario Evandro"
            },
            "vehicle": {
                "type": "gol",
                "plate": "POB3E70"
            }
        }

    def test_enter_parking_200(self):
        response = self.client.post(self.url, data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['vehicle']['plate'], "POB3E70")
        self.assertEqual(response.data['status'], "No estacionamento")

    def test_enter_parking_400_already_in_parking(self):
        _create_parking()
        response = self.client.post(self.url, data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['message'][0]), 'Veículo já está no estacionamento.')


class LeaveParkingTestCase(APITestCase):

    def setUp(self):
        self.parking = _create_parking()
        self.url = reverse(
            "parking:leave_parking",
            kwargs={'parking_lot_id': self.parking.parking_lot.id, 'vehicle_id': self.parking.vehicle.id}
        )

    def test_leave_parking_200(self):
        self.parking.paid_at = datetime.utcnow()
        self.parking.save()

        response = self.client.patch(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['left_at'])

    def test_leave_parking_400_without_payment(self):

        response = self.client.patch(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['message'][0]), 'Pagamento necessário.')

    def test_leave_parking_400_already_left(self):
        self.parking.paid_at = datetime.utcnow()
        self.parking.left_at = datetime.utcnow()
        self.parking.save()
        response = self.client.patch(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['message'][0]), 'O carro já saiu do estacionamento.')


class PayParkingTestCase(APITestCase):

    def setUp(self):
        self.parking = _create_parking()
        self.url = reverse(
            "parking:pay_parking",
            kwargs={'parking_lot_id': self.parking.parking_lot.id, 'vehicle_id': self.parking.vehicle.id}
        )

    def test_pay_parking_200(self):
        self.parking.save()

        response = self.client.patch(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['paid_at'])

    def test_pay_parking_400_already_paid(self):
        self.parking.paid_at = datetime.utcnow()
        self.parking.save()
        response = self.client.patch(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['message'][0]), 'O pagamento já foi realizado.')


class HistoryPlateTestCase(APITestCase):

    def setUp(self):
        self.parking = _create_parking()
        self.url = reverse(
            "parking:history_plate",
            kwargs={'plate': 'POB3E70'}
        )

    def test_history_plate_200(self):

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['status'], 'No estacionamento')
