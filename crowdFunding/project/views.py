from django.shortcuts import render, redirect,get_object_or_404,reverse
from project.models import Project, Category,Picture
from project.forms import ProjectModelForm,CategoryModelForm,TagModelForm
from commentary.forms import CommentForm,ReportForm, ReplyForm
from project.models import Project , Donation
from project.forms import ProjectModelForm,CategoryModelForm,TagModelForm,DonationModelForm,PictureModelForm
from commentary.forms import CommentForm,ReportForm
from commentary.models import Comment
from django.db.models import F
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.files import File
from django.conf import settings
import os
from pathlib import Path
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from django.http import Http404


def hello(request):
    print(request)
    return render(request, 'test.html', {'name': 'Hello'})

@login_required
def create_project_model_form(request):
    if request.method == 'POST':
        form = ProjectModelForm(request.POST, request.FILES)        
        if form.is_valid():
            project = form.save(commit=False)
            project.project_owner = request.user
            project.save()
            form.save_m2m()
            return redirect(project.show_url)
    else:
        form = ProjectModelForm()
        
    return render(request, 'project/forms/createmodel.html', {'form': form})

# def create_project_model_form(request):
#     if request.method == 'POST':
#         form = ProjectModelForm(request.POST, request.FILES)        
#         if form.is_valid():
#             project = form.save(commit=False)
#             project.project_owner = request.user

#             # Save tags associated with the project

#             # Save form_pic instances, associate them with the project
#             for img in request.FILES.getlist('pic'):
#                 if img.content_type in ['image/png', 'image/jpeg', 'image/jpg']:
#                     project.save()
#                     form.save_m2m()
#                     picture_instance = Picture(image=img, project=project)
#                     picture_instance.save()
#                 else:
#                     return JsonResponse({'error': 'Invalid file type only png and jpeg and jpg are allowed', 'x': 0})

#             # Return JSON response with success message and project ID
            
#             return JsonResponse({'success': 'Project created successfully', 'project_id': project.id, 'x': 1})
#     else:
#         form = ProjectModelForm()
        
#     return render(request, 'project/forms/createmodel.html', {'form': form, 'x': 0})





@login_required
def show_category(request, id):
    category = Category.get_category_by_id(id)
    return render(request,'category/crud/show.html', context={"category": category})

@login_required
def project_show(request,id):
    # project = get_object_or_404(Project, pk=id)
    try:
        project = Project.objects.get(pk=id)
    except Project.DoesNotExist:

        return render(request, 'project/crud/badrequest.html')
    images = project.images.all()
    comments = project.comments.all()
    reports = project.reports.all()
    reviews_reply = project.comments.prefetch_related('replies')
    form = CommentForm()
    form2 = ReportForm()
    reply_form = ReplyForm()
    if project.total_target != 0:
        progress_percentage = (project.current_donation / project.total_target) * 100
    else:
        progress_percentage = 0
    return render(request, "project/crud/show.html",
                context={"project": project,'images': images, 'comments': comments, 'reports': reports,
                        'form': form, 'form2': form2, "reply_form":reply_form, "reviews_reply":reviews_reply
                        , 'progress_percentage': progress_percentage})

# def project_show(request,id):
#     project = get_object_or_404(Project, pk=id)
#     comments = Comment.objects.filter(project=project)
#     for comment in comments:
#         comment.stars = range(int(comment.rate))
#         comment.empty_stars = range(5 - int(comment.rate))
#
#     reports = project.reports.all()
#     form = CommentForm()
#     form2 = ReportForm()
#
#     return render(request, "project/crud/show.html",
#                   context={"project":project, 'comments': comments, 'reports': reports, 'form': form, 'form2': form2})
#

@login_required
def cancel_project(request, id):
    try:
        project = Project.objects.get(pk=id)
    except Project.DoesNotExist:

        return render(request, 'project/crud/badrequest.html')
    
    # Check if the current user is the owner of the project
    if request.user == project.project_owner:
        total_target = project.total_target
        donation = project.current_donation
        if donation < total_target * 0.25:
            project.delete()
            return redirect(project.list_url)
        else:
            error_message = 'The donation is greater than 25%'
            # return render(request, 'project/crud/show.html', {'error_message': error_message})
            redirect_url = f"{project.show_url}?error_message={error_message}"
            return redirect(redirect_url)
            
    else:
        # If the current user is not the owner, handle unauthorized access
        # For example, you can return a 403 Forbidden response or redirect to a different page
        return HttpResponseForbidden("You are not authorized to perform this action.") 

def list_project(request):
    projects = Project.objects.all()
    return render(request, 'project/crud/list.html', {'projects': projects})


@login_required
def donate_project(request, id):
    try:
        project = Project.objects.get(pk=id)
    except Project.DoesNotExist:

        return render(request, 'project/crud/badrequest.html')
    
    if project.is_run_project() == False:
        return HttpResponseForbidden("the project is not run")
    
    
    if request.method == 'POST':
        form = DonationModelForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.project = project
            donation.user = request.user
            donation.save()
            
            # Increase the current donation for the project
            project.current_donation += donation.donation
            project.save()
            # Redirect to project details page or any other desired page
            return redirect(project.show_url, id=id, project=project)  

    else:
        form = DonationModelForm()

    return render(request, 'project/crud/donate.html', {'form': form, 'project': project})



@login_required
def edit_project(request, id):
    project=Project.get_project_by_id(id)
    form=ProjectModelForm(instance=project)
    if request.method == "POST":
        form=ProjectModelForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project=form.save()
            return redirect(project.show_url)

    return render (request,'project/crud/edit.html', context={"form":form})


@login_required
def add_images(request, id):
    try:
        project = Project.objects.get(pk=id)
    except Project.DoesNotExist:

        return render(request, 'project/crud/badrequest.html')
    if request.method == 'POST':
        form = PictureModelForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the list of image files from the request
            image_files = request.FILES.getlist('image')

            # Iterate over each image file
            for image_file in image_files:
                # Create a new Picture instance
                picture = Picture(image=image_file, project=project)
                picture.save()

            # Redirect or render a success page
            return redirect(project.show_url)
    else:
        form = PictureModelForm()
    return render(request, 'project/forms/add_image.html', {'form': form})


@login_required
def edit_images(request, id):
    project = get_object_or_404(Project, pk=id)
    if request.method == 'POST':
        form = PictureModelForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the list of image files from the request
            image_files = request.FILES.getlist('image')

            # Iterate over each image file
            for image_file in image_files:
                # Create a new Picture instance
                picture = Picture(image=image_file, project=project)
                picture.save()

            # Redirect or render a success page
            return redirect(project.show_url)
    else:
        form = PictureModelForm()
    return render(request, 'project/forms/edit_image.html', {'form': form})

def clear_images(request, id):
    try:
        project = Project.objects.get(pk=id)
    except Project.DoesNotExist:

        return render(request, 'project/crud/badrequest.html')
    for picture in project.images.all():
            picture.image.delete()  # This will delete the image file from the storage
            picture.delete()  # This will delete the Picture instance from the database
    return redirect(project.show_url)
     

        