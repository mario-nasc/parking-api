from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from apps.parking.api.serializers import EnterParkingSerializer, LeaveParkingSerializer, PayParkingSerializer, PlateHistoryParkingSerializer
from apps.parking.models import Parking
from datetime import datetime

from apps.control.models import Vehicle


class ParkingViewSet(viewsets.ViewSet):

    def enter_parking(self, request, parking_lot_id):
        serializer = EnterParkingSerializer(data=request.data, parking_lot_id=parking_lot_id)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)

    def leave_parking(self, _, parking_lot_id, vehicle_id):
        parking = get_object_or_404(Parking, vehicle_id=vehicle_id, parking_lot_id=parking_lot_id)
        serializer = LeaveParkingSerializer(parking, {'left_at': datetime.utcnow()})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)

    def pay_parking(self, _, parking_lot_id, vehicle_id):
        parking = get_object_or_404(Parking, vehicle_id=vehicle_id, parking_lot_id=parking_lot_id)
        serializer = PayParkingSerializer(parking, {'paid_at': datetime.utcnow()})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)

    def history_plate(self, _, plate):
        vehicle = get_object_or_404(Vehicle, plate=plate)
        parkings = Parking.objects.filter(vehicle=vehicle)
        serializer = PlateHistoryParkingSerializer(parkings, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
