from datetime import datetime
from django.db.models import Q
from rest_framework import serializers

from apps.control.models import Client, Vehicle
from apps.parking.models import Parking


class ClientSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_null=True)
    cellphone = serializers.CharField()


class VehicleSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    plate = serializers.RegexField(r'^[A-Z]{3}\d{1}[A-Z]{1}\d{2}$')
    type = serializers.CharField()


class VehicleFullSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    plate = serializers.RegexField(r'^[A-Z]{3}\d{1}[A-Z]{1}\d{2}$')
    type = serializers.CharField()
    client = ClientSerializer()


class ParkingLotSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_null=True)



class EnterParkingSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    client = ClientSerializer()
    vehicle = VehicleSerializer()

    def __init__(self, *args, **kwargs):
        self.parking_lot_id = kwargs.pop('parking_lot_id', None)
        super().__init__(*args, **kwargs)

    def validate(self, data):
        if Parking.objects.filter(vehicle__plate=data['vehicle']['plate']).filter((Q(paid_at__isnull=True) | Q(left_at__isnull=True))):
            raise serializers.ValidationError({'message': 'Veículo já está no estacionamento.'})
        return data

    def create(self, validated_data):
        client, _ = Client.objects.get_or_create(**validated_data['client'])
        vehicle, _ = Vehicle.objects.get_or_create(client=client, **validated_data['vehicle'])
        parking = Parking.objects.create(
            vehicle=vehicle,
            parking_lot_id=self.parking_lot_id
        )
        validated_data['id'] = parking.id
        validated_data['vehicle']['id'] = vehicle.id
        return validated_data


class LeaveParkingSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(required=False)
    parking_lot = ParkingLotSerializer(required=False)

    class Meta:
        model = Parking
        fields = '__all__'

    def validate(self, data):
        if not self.instance.paid_at:
            raise serializers.ValidationError({'message': 'Pagamento necessário.'})
        if self.instance.left_at:
            raise serializers.ValidationError({'message': 'O carro já saiu do estacionamento.'})
        return data


class PayParkingSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(required=False)
    parking_lot = ParkingLotSerializer(required=False)

    class Meta:
        model = Parking
        fields = '__all__'

    def validate(self, data):
        if self.instance.paid_at:
            raise serializers.ValidationError({'message': 'O pagamento já foi realizado.'})
        return data


class PlateHistoryParkingSerializer(serializers.ModelSerializer):
    vehicle = VehicleFullSerializer(required=False)
    parking_lot = ParkingLotSerializer(required=False)
    time = serializers.SerializerMethodField()

    class Meta:
        model = Parking
        fields = ('id', 'vehicle', 'parking_lot', 'status', 'time')

    def get_time(self, obj):
        if obj.left_at:
            return f'{round((obj.left_at - obj.started_at).total_seconds()/60)} minutes'
        else:
            return f'{round((datetime.utcnow() - obj.started_at.replace(tzinfo=None)).total_seconds()/60)} minutes'
