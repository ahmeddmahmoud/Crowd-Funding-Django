from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import UserRegistrationForm,UserEditForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout,get_user_model
from users.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from typing import Protocol
from .tokens import account_activation_token
from project.models import Project,Donation
from django.db.models import Sum




def index(request):
    return render(request, 'users/index.html')


def login_form(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Hello {user.first_name}! You have been logged in")
                if user.is_superuser:
                    return redirect('index')
                else:
                    url = reverse('user.details', args=[user.id])
                    return redirect(url)

    return render(request, 'users/login.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        # Handle decoding errors or user not found
        messages.error(request, "Invalid activation link.")
        return redirect('index')

    if account_activation_token.check_token(user, token):
        # Activate the user account
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated successfully. You can now log in.")
        return redirect('user.login')
    else:
        # Invalid token
        messages.error(request, "Invalid activation link.")
        return redirect('index')


def activate_email(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.first_name,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user.first_name}!, please go to you email {to_email}! inbox and click on \
                               received activation link to confirm and complete the registration. Note!: Check your spam folder.')

    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


def register(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user=form.save()
            activate_email(request, user, form.cleaned_data.get('email'))
            login_url = reverse("index")
            return redirect(login_url)
    return render(request, 'users/register.html', {'form': form})


@login_required
def user_details(request, id):
    user = get_object_or_404(User, pk=id)
    if request.user != user:
        return render(request, 'users/unauthorized.html')
    return render(request, 'users/user_details.html', {'user': user})


@login_required
def user_delete(request, id):
    user = get_object_or_404(User, pk=id)
    user.delete()
    url = reverse("user.login")
    return redirect(url)

@login_required
def user_edit(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            url = reverse("user.details",args=[user.id])
            return redirect(url)
    else:
        form = UserEditForm(instance=user)
    
    return render(request, 'users/user_edit.html', {'form': form})


def featured_projects(request):
    data = Project.objects.all()
    return render(request, 'admin/featured_projects.html', {'data': data})


# def add_to_featured(request, id):
#     project = get_object_or_404(Project, pk=id)
#     # Check if the project is already featured
#     if not FeaturedProject.objects.filter(project=project).exists():
#         # If not featured, create a FeaturedProject instance
#         FeaturedProject.objects.create(project=project)
#         # Redirect to a success URL or back to the project list page
#     return redirect('featured')

@login_required
def user_donations(request,id) :
    user = User.objects.get(id=id)

    if request.user != user:
        return render(request, 'users/unauthorized.html')

    total_donation_user = Donation.objects.filter(user=user).aggregate(total_donation_user=Sum('donation'))['total_donation_user']
    if total_donation_user is None:
        total_donation_user = 0.0

    project_donations = Donation.objects.filter(user=user).values('project_id', 'project__title').annotate(total_donation_project=Sum('donation'))

    for donation in project_donations:
        donation['user_donations'] = Donation.objects.filter(user=user, project_id=donation['project_id']).order_by('-created_at')

    return render(request, 'users/user_donations.html', {
        'user': user,
        'total_donation_user': total_donation_user,
        'project_donations': project_donations
    })
