from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import (UserRegistrationForm,UserEditForm,UserAddFormByAdmin,UserEditFormByAdmin)
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
from django import forms

from .tokens import account_activation_token
from project.models import Project, Category, Tag
from project.forms import CategoryModelForm, TagModelForm
from project.models import Project,Donation
from django.db.models import Sum
from django.utils import timezone




# @login_required
def index(request):
    projects=Project.objects.all()
    latest_books = projects.order_by('-created_at')[:5]
    latest_featured_projects = Project.objects.filter(is_featured=True).order_by('-featured_at')[:5]
    for project in latest_books:
        project.progress_donation=(project.current_donation / project.total_target) * 100

    sorted_products = sorted(projects, key=lambda p: p.rate, reverse=True)

    # Get the top five products
    top_five_products = sorted_products[:5]
    print("Top Five Product Rates:")
    for product in top_five_products:
        print(f"Product: {product.title}, Rate: {product.rate}")
    return render(request , 'users/index.html' ,
                  context={"projects" : projects,"latest_books":latest_books,
                           "top_five_products": top_five_products, "latest_featured_projects":latest_featured_projects
                           })


def login_form(request):
    if request.user.is_authenticated:
        messages.error(request, "You are already logged in.")
        return redirect('index')
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
                    return redirect('admin.dashboard')
                else:
                    url = reverse('index')
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
    user_exists = User.objects.filter(id=id).exists()
    if not user_exists:
        return render(request, 'users/unauthorized.html')
    user = get_object_or_404(User, pk=id)
    if request.user != user:
        return render(request, 'users/unauthorized.html')
    return render(request, 'users/user_details.html', {'user': user})


@login_required 
def user_delete(request, id):
    if not request.user.id == id:
        messages.error(request, "Unauthorized attempt to delete user.")
        return redirect('index')
    user = get_object_or_404(User, pk=id)
    user.delete()
    logout(request)  
    messages.success(request, "Your account has been successfully deleted.")
    return redirect('home_page')

@login_required
def user_edit(request, id):    
    user_exists = User.objects.filter(id=id).exists()
    if not user_exists:
        return render(request, 'users/unauthorized.html')
    user = get_object_or_404(User, pk=id)
    if request.user != user:
        return render(request, 'users/unauthorized.html')
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
    projects = Project.objects.all()
    return render(request, 'admin/featured_projects.html', {'projects': projects})


def add_to_featured(request, id):
    project = get_object_or_404(Project, pk=id)

    # Toggle is_featured value
    project.is_featured = not project.is_featured
    if project.is_featured:
        project.featured_at = timezone.now()
    else:
        project.featured_at = None
    project.save()
    return redirect('featured')


def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')


def add_category(request):
    form = CategoryModelForm()

    if request.method == 'POST':
        form = CategoryModelForm(request.POST)  # Bind POST data to the form
        if form.is_valid():
            category = form.save()
            return redirect('category.index')

    return render(request, 'admin/add_category.html', {'form': form})


def category_index(request):
    categories=Category.objects.all()
    return render(request,'admin/category_index.html', context={"categories":categories})


def edit_category(request, id):
    category = Category.get_category_by_id(id)
    form = CategoryModelForm(instance=category)
    if request.method == "POST":
        form = CategoryModelForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            category = form.save()
            return redirect("category.index")

    return render(request,'admin/edit_category.html', context={"form": form})


def delete_category(request, id):
    category = get_object_or_404(Category, pk=id)
    category.delete()
    return redirect("category.index")


def tag_index(request):
    tags=Tag.objects.all()
    return render(request,'admin/tag_index.html', context={"tags":tags})


def add_tag(request):
    form = TagModelForm()
    if request.method == 'POST':
        form = TagModelForm(request.POST)
        if form.is_valid():
            tag = form.save()
            return redirect('tag.index')
    return render(request, 'admin/add_tag.html',context={'form': form})


def edit_tag(request, id):
    tag = Tag.get_tag_by_id(id)
    form = TagModelForm(instance=tag)
    if request.method == "POST":
        form = TagModelForm(request.POST, instance=tag)
        if form.is_valid():
            category = form.save()
            return redirect("tag.index")

    return render(request,'admin/edit_tag.html', context={"form": form})


def delete_tag(request, id):
    tag = get_object_or_404(Tag, pk=id)
    tag.delete()
    return redirect("tag.index")


def user_index(request):
    users = User.objects.all()
    return render(request, 'admin/user_index.html', context={"users": users})


def delete_user_by_admin(request, id):
    user = get_object_or_404(User, pk=id)
    user.delete()
    return redirect("user.index")


def add_user_by_admin(request):
    form = UserAddFormByAdmin()
    if request.method == 'POST':
        form = UserAddFormByAdmin(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            if not user.is_active:
                activate_email(request, user, form.cleaned_data.get('email'))
            return redirect("user.index")
    return render(request, 'admin/add_user_by_admin.html', {'form': form})


def edit_user_by_admin(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = UserEditFormByAdmin(request.POST, request.FILES, instance=user)
        if form.is_valid():
            # Save the form without committing to get the user object
            user = form.save(commit=False)

            # Check if password fields are provided
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password1 and password2 and password1 == password2:
                # Set the password only if both passwords match
                user.set_password(password1)

            # Save the user object with updated password
            user.save()

            return redirect("user.index")
    else:
        form = UserEditFormByAdmin(instance=user)

    return render(request, 'admin/edit_user_by_admin.html', {'form': form})


@login_required
def user_donations(request,id) :

    user_exists = User.objects.filter(id=id).exists()
    if not user_exists:
        return render(request, 'users/unauthorized.html')
    
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

@login_required
def user_projects(request, id):

    user_exists = User.objects.filter(id=id).exists()
    if not user_exists:
        return render(request, 'users/unauthorized.html')

    user = User.objects.get(id=id)

    if request.user != user:
        return render(request, 'users/unauthorized.html')

    projects = Project.objects.filter(project_owner_id=id)

    return render(request, 'users/user_projects.html', {
        'user': user,
        'projects': projects,
    })

@login_required
def categories_project(request):
    categories = Category.objects.all().prefetch_related('project_set')
    return render(request, 'users/categories_projects.html', {
        'categories': categories
    })

@login_required
def user_logout(request):
    logout(request)
    # messages.info(request, "You have been successfully logged out.")
    url = reverse("home_page")
    return redirect(url)
