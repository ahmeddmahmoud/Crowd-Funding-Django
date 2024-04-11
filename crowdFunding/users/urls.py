from django.urls import path,include
from users.views import create_user,index,login
urlpatterns = [
    path('register/', create_user, name="user.register"),
    path('', index, name="index"),
    path('login/', login, name="user.login"),
]
