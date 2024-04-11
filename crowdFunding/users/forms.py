from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from users.models import CustomUser


# from django.core.exceptions import ValidationError
# from django.contrib.auth import get_user_model
# from .models import Profile
# from django.contrib.auth.forms import AuthenticationForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "profile_picture"]
        # fields
# , "mobile_phone", "email", "password1", "password2", "mobile_phone", "first_name", "last_name",


# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = CustomUser
#         fields = ["username", "profile_picture"]