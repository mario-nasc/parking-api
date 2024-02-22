from django.urls import path

from apps.parking.api.viewsets import ParkingViewSet
from apps.parking.views import ParkingView


urlpatterns = [
    path('api/enter-parking/<int:parking_lot_id>', ParkingViewSet.as_view({'post': 'enter_parking'}), name='enter_parking'),
    path(
        'api/leave-parking/<int:parking_lot_id>/<int:vehicle_id>',
        ParkingViewSet.as_view({'patch': 'leave_parking'}),
        name='leave_parking'),
    path(
        'api/pay-parking/<int:parking_lot_id>/<int:vehicle_id>',
        ParkingViewSet.as_view({'patch': 'pay_parking'}),
        name='pay_parking'),
    path(
        'api/history-plate/<str:plate>',
        ParkingViewSet.as_view({'get': 'history_plate'}),
        name='history_plate'),
    path('', ParkingView.as_view(), name='parking_view'),
]
