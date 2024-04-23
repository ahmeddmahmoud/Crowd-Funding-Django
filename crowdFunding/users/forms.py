from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.validators import URLValidator
from datetime import date



class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'phone', 'photo']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        if not email:
            raise forms.ValidationError('Email is required')
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise forms.ValidationError('First name is required')
        if not first_name.isalpha():
            raise forms.ValidationError('First name must be alphabetic')
        if len(first_name) < 3:
            raise forms.ValidationError('First name must be at least 3 characters long')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name:
            raise forms.ValidationError('Last name is required')
        if not last_name.isalpha():
            raise forms.ValidationError('Last name must be alphabetic')
        if len(last_name) < 3:
            raise forms.ValidationError('Last name must be at least 3 characters long')
        return last_name

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone:
            raise forms.ValidationError('Mobile phone is required')
        if not phone.startswith('01'):
            raise forms.ValidationError('Mobile phone must start with 01')
        if not phone.isdigit():
            raise forms.ValidationError('Mobile phone must be digits')
        return phone

    def clean_photo(self):
        photo = self.cleaned_data['photo']
        if not photo:
            raise forms.ValidationError('Photo is required')
        return photo

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if not password1:
            raise forms.ValidationError('Password is required')

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if not password2:
            raise forms.ValidationError('Password is required')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')

        return password2


class UserEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['email'].disabled = True

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise forms.ValidationError('First name is required')
        if not first_name.isalpha():
            raise forms.ValidationError('First name must be alphabetic')
        if len(first_name) < 3:
            raise forms.ValidationError('First name must be at least 3 characters long')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name:
            raise forms.ValidationError('Last name is required')
        if not last_name.isalpha():
            raise forms.ValidationError('Last name must be alphabetic')
        if len(last_name) < 3:
            raise forms.ValidationError('Last name must be at least 3 characters long')
        return last_name

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone:
            raise forms.ValidationError('Mobile phone is required')
        if not phone.startswith('01'):
            raise forms.ValidationError('Mobile phone must start with 01')
        if not phone.isdigit():
            raise forms.ValidationError('Mobile phone must be digits')
        return phone
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        if birth_date and birth_date > date.today():
            raise forms.ValidationError('Birth date cannot be in the future.')
        return birth_date
    
    def clean_facebook(self):
        facebook = self.cleaned_data['facebook']
        if facebook:
            validator = URLValidator()
            validator(facebook)
            if "facebook.com" not in facebook:
                raise forms.ValidationError('Please enter a valid Facebook URL.')
        return facebook
    
    def clean_country(self):
        country = self.cleaned_data['country']
        if not country.isalpha():
            raise forms.ValidationError('country name must be alphabetic')
        if len(country) < 3:
            raise forms.ValidationError('country name must be at least 3 characters long')
        return country
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'birth_date', 'country', 'facebook', 'photo']
        widgets = {
            'facebook': forms.URLInput(attrs={'class': 'form-control'}),
        }
    





class UserAddFormByAdmin(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1','password2', 'phone', 'photo', 'is_superuser', 'is_staff', 'is_active']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Email already exists')
        if not email:
            raise forms.ValidationError('Email is required')
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise forms.ValidationError('First name is required')
        if not first_name.isalpha():
            raise forms.ValidationError('First name must be alphabetic')
        if len(first_name) < 3:
            raise forms.ValidationError('First name must be at least 3 characters long')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name:
            raise forms.ValidationError('Last name is required')
        if not last_name.isalpha():
            raise forms.ValidationError('Last name must be alphabetic')
        if len(last_name) < 3:
            raise forms.ValidationError('Last name must be at least 3 characters long')
        return last_name

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone:
            raise forms.ValidationError('Mobile phone is required')
        if not phone.startswith('01'):
            raise forms.ValidationError('Mobile phone must start with 01')
        if not phone.isdigit():
            raise forms.ValidationError('Mobile phone must be digits')
        return phone

    def clean_photo(self):
        photo = self.cleaned_data['photo']
        if not photo:
            raise forms.ValidationError('Photo is required')
        return photo

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if not password1:
            raise forms.ValidationError('Password is required')

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if not password2:
            raise forms.ValidationError('Password is required')
        if password1 != password2:
            raise forms.ValidationError('Passwords do not match')

        return password2


class UserEditFormByAdmin(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1','password2', 'phone', 'photo', 'is_superuser', 'is_staff', 'is_active']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


    def clean_photo(self):
        photo = self.cleaned_data['photo']
        if not photo:
            raise forms.ValidationError('Photo is required')
        return photo