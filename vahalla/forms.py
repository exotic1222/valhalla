from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Reservation, Profile

User = get_user_model()

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['event_date', 'event_time', 'reservation_type', 'mesa_number', 'num_people', 'price']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    address = forms.CharField(max_length=255, required=True)
    phone = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'address', 'phone']