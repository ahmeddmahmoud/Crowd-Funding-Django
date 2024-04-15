from django.shortcuts import render, redirect, reverse
from users.forms import RegistrationForm
from users.models import CustomUser


def index(request):
    return render(request,'users/index.html')


def login(request):

    return render(request,'users/login.html')

def create_user(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login_url = reverse("index")
            return redirect(login_url)

    return render(request,'users/register.html',{'form': form})

def user_details(request):
    CustomUser.objects.get(id=0)

    return render(request,'users/user_details.html' )

def user_home(request):
    pass

def user_projects(request):
    return render(request,'users/user_projects.html' )

def user_donations(request):
    return render(request,'users/user_donations.html' )