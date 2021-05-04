from django.contrib.auth.forms import UserCreationForm
from django.forms import forms

from .models import CustomUser


class CustomUserSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('login', 'email', 'role', 'phone', 'club')
