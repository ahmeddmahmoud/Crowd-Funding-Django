from project.views import (hello )
from django.urls import path

urlpatterns = [
    path("hello", hello, name= "hello"),
   

]