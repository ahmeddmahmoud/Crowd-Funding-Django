from project.views import (hello, create_project_model_form )
from django.urls import path

urlpatterns = [
    path("hello", hello, name= "hello"),
    path('createform', create_project_model_form, name='project.createmodel')
]