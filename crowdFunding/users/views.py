from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from users.models import User
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request,'users/index.html')


def login_form(request):
    form=AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                url = reverse('user.details', args=[user.id])
                return redirect(url)
            
    return render(request,'users/login.html',{'form':form})


def register(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            login_url = reverse("index")
            return redirect(login_url)
    return render(request, 'users/register.html', {'form': form})

@login_required
def user_details(request,id):
    user = get_object_or_404(User, pk=id)
    return render(request,'users/user_details.html',{'user': user} )

