from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.core.validators import RegexValidator


class CustomUser(User):
# class CustomUser(AbstractUser):

#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     username = models.CharField(max_length=100)
#     email = models.EmailField(max_length=100)

    # mobile_regex = RegexValidator(regex=r'^20(10|11|12|15)\d{8}$', message="Enter a valid Egyptian phone number")
    # mobile_phone = models.CharField(validators=[mobile_regex], max_length=11)
    profile_picture = models.ImageField(upload_to="users/images/",null=True,blank=True)
    birth_date = models.DateField(null=True,blank=True)
    facebook_profile = models.URLField(null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)



    def __str__(self):
        return self.username
    @property
    def profile_picture_url(self):
        return f"/media/{self.profile_picture}"

    # password = models.CharField(max_length=100)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
