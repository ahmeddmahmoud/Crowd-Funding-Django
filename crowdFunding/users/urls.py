from django.urls import path,include
from users.views import user_details,login_form,register,index, user_delete,activate
urlpatterns = [
    path('register/', register, name="user.register"),
    path('', index, name="index"),
    path('login/', login_form, name="user.login"),
    path('details/<int:id>',user_details , name="user.details"),
    path('delete/<int:id>',user_delete , name="user.delete"),
    path('activate/<uidb64>/<token>', activate, name='activate')

]