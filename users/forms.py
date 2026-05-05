from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil


class RegistroForm(UserCreationForm):

    telefono = forms.CharField(
        label="Teléfono",
        help_text="Ingresa tu número (WhatsApp recomendado)",
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej: 77712345'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'telefono', 'password1', 'password2']