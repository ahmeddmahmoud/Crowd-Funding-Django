from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'phone', 'photo']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.startswith('01'):
            raise forms.ValidationError('Mobile phone must start with 01')
        return phone
