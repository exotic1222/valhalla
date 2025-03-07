from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['event_date', 'event_time', 'reservation_type', 'mesa_number', 'num_people', 'price']