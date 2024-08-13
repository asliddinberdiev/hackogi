from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser

class CustomLoginForm(AuthenticationForm):
    pass


class RegisterFrom(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'email',
            'password1',
            'password2'
        )
