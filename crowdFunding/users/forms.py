from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError
# from django.contrib.auth import get_user_model
# from .models import Profile
# from django.contrib.auth.forms import AuthenticationForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = "__all__"
        # fields
