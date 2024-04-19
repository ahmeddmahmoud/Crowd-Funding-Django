from project.views import (hello, create_project_model_form, create_category,create_Tag,
    list_project, cancel_project,project_show, donate_project, edit_project,
                           index_category, delete_category, show_category, edit_category)
from commentary.views import add_comment
from django.urls import path

urlpatterns = [
    path("hello", hello, name= "hello"),
    path('<int:id>/comment', add_comment, name='project.comment'),
    path('createproject', create_project_model_form, name='project.createmodel'),
    path('createcategory', create_category, name='project.createcategory'),
    path('createtag' , create_Tag, name ='project.createtag'),
    path('<int:id>', project_show, name='project.show'),
    path('cancelproject/<int:id>', cancel_project, name='project.cancel'),
    path('', list_project, name='project.list'),
    path('donate/<int:id>', donate_project, name='project.donate'),
    path('<int:id>/edit', edit_project, name='project.edit'),
    path('category/', index_category, name='category.index'),
    path('category/<int:id>/delete', delete_category, name='category.delete'),
    path('category/<int:id>/show', show_category, name='category.show'),
    path('category/<int:id>/edit', edit_category, name='category.edit'),

]