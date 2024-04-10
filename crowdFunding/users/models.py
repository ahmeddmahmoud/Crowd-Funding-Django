from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    mobile_regex = RegexValidator(regex=r'^20(10|11|12|15)\d{8}$', message="Enter a valid Egyptian phone number")
    mobile_phone=models.CharField(validators=[mobile_regex], max_length=11, unique=True)
    profile_picture=models.ImageField(upload_to="users/images/",null=True,blank=True)

    # password = models.CharField(max_length=100)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
