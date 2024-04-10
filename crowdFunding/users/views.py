from django.shortcuts import render, redirect, reverse
from users.forms import RegistrationForm

# Create your views here.


def create_user(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login_url=reverse("login")
            return redirect(login_url)

    return render(request,'users/register.html',{'form':form})