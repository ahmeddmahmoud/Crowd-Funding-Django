from django.urls import path
from commentary.views import add_comment


urlpatterns = [
    path('comment', add_comment, name='projects.comment')
]
