from project.views import (hello, create_project_model_form, create_category,create_Tag,
                           project_show)
from django.urls import path

urlpatterns = [
    path("hello", hello, name= "hello"),
    path('createproject', create_project_model_form, name='project.createmodel'),
    path('creaetecategory', create_category, name='project.createcategory'),
    path('createtag' , create_Tag, name ='project.createtag'),
    path('<int:id>', project_show, name='project.show' )
]