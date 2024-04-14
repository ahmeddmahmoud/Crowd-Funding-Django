from django.shortcuts import render, redirect,get_object_or_404,reverse
from project.models import Project
from project.forms import ProjectModelForm,CategoryModelForm,TagModelForm


def hello(request):
    print(request)
    return render(request, 'test.html', {'name': 'Hello'})


def create_project_model_form(request):
    form = ProjectModelForm()
    if request.method == 'POST':
        form = ProjectModelForm(request.POST, request.FILES)
        if form.is_valid():
            project=form.save()
            return redirect(project.show_url)

    return render(request,'project/forms/createmodel.html',
                context={"form": form})


def create_category(request):
    form = CategoryModelForm()

    if request.method == 'POST':
        form = CategoryModelForm(request.POST)  # Bind POST data to the form
        if form.is_valid():
            category = form.save()
            #return redirect('category_detail', pk=category.pk)  # Redirect to category detail view
        # If form is not valid, it will render the form again with validation errors

    return render(request, 'project/forms/createCategory.html', {'form': form})

def create_Tag(request):
    form= TagModelForm()
    if request.method == 'POST':
        form = TagModelForm(request.POST)
        if form.is_valid():
            tag = form.save()

    return render(request, 'project/forms/createTag.html',
                context={'form': form})

def project_show(request,id):
    project = get_object_or_404(Project, pk=id)
    return render(request, "project/crud/show.html",
                context={"project":project})


def cancel_project(request,id):
    project = get_object_or_404(Project, pk=id)
    total_target = project.total_target
    donation = project.current_donation
    if donation < total_target*0.25:
        project.delete()
        return redirect('hello')
    else:
        return redirect(project.show_url)
    
    
def list_project(request):
    projects = Project.objects.all()
    return render(request, 'project/crud/list.html', {'projects': projects})



