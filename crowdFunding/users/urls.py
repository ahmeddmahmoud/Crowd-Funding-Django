from django.urls import path,include
from users.views import register,index,login_form
urlpatterns = [
    path('register/', register, name="user.register"),
    path('', index, name="index"),
    path('login/', login_form, name="user.login"),
    # path('details',user_details , name="user.details")
]