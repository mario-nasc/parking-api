from django.views.generic import ListView

from apps.parking.models import Parking


class ParkingView(ListView):
    model = Parking
    context_object_name = 'parkings'
