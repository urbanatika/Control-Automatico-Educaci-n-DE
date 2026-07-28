from django.contrib.auth.forms import UserCreationForm

from .models import User


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["email", "username", "first_name", "last_name"]
        labels = {
            "email": "Correo electrónico",
            "username": "Nombre de usuario",
            "first_name": "Nombre",
            "last_name": "Apellido",
        }
