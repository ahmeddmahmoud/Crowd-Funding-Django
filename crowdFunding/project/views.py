from django.shortcuts import render, redirect,get_object_or_404,reverse
from project.models import Project, Category
from project.forms import ProjectModelForm,CategoryModelForm,TagModelForm
from commentary.forms import CommentForm,ReportForm, ReplyForm
from project.models import Project , Donation
from project.forms import ProjectModelForm,CategoryModelForm,TagModelForm,DonationModelForm,PictureModelForm
from commentary.forms import CommentForm,ReportForm
from commentary.models import Comment
from django.db.models import F

from django.http import HttpResponse

def hello(request):
    print(request)
    return render(request, 'test.html', {'name': 'Hello'})


from .forms import ProjectModelForm, PictureModelForm

def create_project_model_form(request):
    if request.method == 'POST':
        form = ProjectModelForm(request.POST)        
        if form.is_valid():
            project = form.save(commit=False)
            project.project_owner = request.user
            project.save()

            # Save form_pic instances, associate them with the project
            for img in request.FILES.getlist('pic'):
                picture_instance = Picture(image=img, project=project)
                picture_instance.save()

            return redirect(project.show_url)  # Assuming there's a show_url method in your Project model
    else:
        form = ProjectModelForm()
        

    return render(request, 'project/forms/createmodel.html', {'form': form})





def create_category(request):
    form = CategoryModelForm()

    if request.method == 'POST':
        form = CategoryModelForm(request.POST)  # Bind POST data to the form
        if form.is_valid():
            category = form.save()
            #return redirect('category_detail', pk=category.pk)  # Redirect to category detail view
        # If form is not valid, it will render the form again with validation errors

    return render(request, 'project/forms/createCategory.html', {'form': form})


def index_category(request):
    categories=Category.objects.all()
    return render(request,'category/crud/index.html', context={"categories":categories})


def show_category(request, id):
    category = Category.get_category_by_id(id)
    return render(request,'category/crud/show.html', context={"category": category})


def edit_category(request, id):
    category = Category.get_category_by_id(id)
    form = CategoryModelForm(instance=category)
    if request.method == "POST":
        form = CategoryModelForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            category = form.save()
            return redirect(category.show_url)

    return render(request,'category/crud/edit.html', context={"form": form})


def delete_category(request, id):
    category = get_object_or_404(Category, pk=id)
    category.delete()
    url=reverse("category.index")
    return redirect(url)


def create_Tag(request):
    form = TagModelForm()
    if request.method == 'POST':
        form = TagModelForm(request.POST)
        if form.is_valid():
            tag = form.save()

    return render(request, 'project/forms/createTag.html',
                context={'form': form})


def project_show(request,id):
    project = get_object_or_404(Project, pk=id)
    comments = project.comments.all()
    reports = project.reports.all()
    reviews_reply = project.comments.prefetch_related('replies')
    form = CommentForm()
    form2 = ReportForm()
    reply_form = ReplyForm()
    return render(request, "project/crud/show.html",
                context={"project": project, 'comments': comments, 'reports': reports,
                         'form': form, 'form2': form2, "reply_form":reply_form, "reviews_reply":reviews_reply})

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


def cancel_project(request,id):
    project = get_object_or_404(Project, pk=id)
    total_target = project.total_target
    donation = project.current_donation
    if donation < total_target*0.25:
        project.delete()
        # return redirect('hello')
    else:
        return redirect(project.show_url)
    
def list_project(request):
    projects = Project.objects.all()
    return render(request, 'project/crud/list.html', {'projects': projects})



def donate_project(request, id):
    project = get_object_or_404(Project, pk=id)
    
    if request.method == 'POST':
        form = DonationModelForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.project = project
            donation.user = request.user
            donation.save()
            
            # Increase the current donation for the project
            Project.objects.filter(pk=project.pk).update(current_donation=F('current_donation') + donation.donation)

            # Redirect to project details page or any other desired page
            return redirect(project.show_url, id=id)  

    else:
        form = DonationModelForm()

    return render(request, 'project/crud/donate.html', {'form': form, 'project': project})


# def donate_project(request, id):
#     if request.method == 'POST':
#         project = get_object_or_404(Project, pk=id)
#         donation_amount = float(request.POST.get('donation_amount'))
        
#         # Create a new Donation object
#         donation = Donation.objects.create(donation=donation_amount, project=project, user=request.user)
        
#         # Update the current_donation field of the Project
#         project.current_donation += donation_amount
#         project.save()

#         return HttpResponse("Donation successful!")  # You can customize this response as needed

#     else:
#         return HttpResponse("Invalid request method")


def edit_project(request, id):
    project=Project.get_project_by_id(id)
    form=ProjectModelForm(instance=project)
    if request.method == "POST":
        form=ProjectModelForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project=form.save()
            return redirect(project.show_url)

    return render (request,'project/crud/edit.html', context={"form":form})

