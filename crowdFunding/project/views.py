from django.shortcuts import render, redirect,get_object_or_404,reverse
from project.models import Project
from project.forms import ProjectModelForm


def hello(request):
    print(request)
    return render(request, 'test.html', {'name': 'Hello'})


def create_project_model_form(request):
    form = ProjectModelForm()
    if request.method == 'POST':
        form = ProjectModelForm(request.POST, request.FILES)
        if form.is_valid():
            project=form.save()
            # return redirect(project.show_url)

    return render(request,'project/forms/createmodel.html',
                  context={"form":form})