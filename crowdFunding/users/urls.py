from django.urls import path,include
from users.views import create_user,index,login,user_details,user_home, user_projects, user_donations
urlpatterns = [
    path('register/', create_user, name="user.register"),
    path('', index, name="index"),
    path('login/', login, name="user.login"),
    path('home',user_home , name="user.home"),
    path('projects',user_projects , name="user.projects"),
    path('donations',user_donations , name="user.donations"),
    path('details',user_details , name="user.details"),]


# from users.views import create_user,index,login,user_details
# urlpatterns = [
#     # path('register/', create_user, name="user.register"),
#     # path('', index, name="index"),
#     # path('login/', login, name="user.login"),
#     # path('details',user_details , name="user.details")
# ]
