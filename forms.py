from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    telefono = forms.CharField(max_length=15, required=False)
    direccion = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'telefono', 'direccion']