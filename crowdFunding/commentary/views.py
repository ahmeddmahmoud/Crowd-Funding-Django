from django.shortcuts import render, redirect, get_object_or_404

from .models import Project, Comment
from .forms import CommentForm, ReportForm

# Create your views here.



def add_comment(request, id) :
    project = get_object_or_404(Project, pk=id)
    if request.method == 'POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.project=project
            comment.user=request.user
            comment.save()
            return redirect('project/crud/show.html',id=id)
    else:
        form = CommentForm()
        return render(request, 'project/crud/show.html', {'form': form})




def add_report(request, id, comment_id=None):
    project = get_object_or_404(Project, pk=id)
    comment = None

    if comment_id:
        comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            status = form.cleaned_data['status']

            report = form.save(commit=False)
            report.project = project
            report.user = request.user
            report.comment = comment
            report.save()

            return redirect('project.show', id=id)

    else:
        form = ReportForm()

    return render(request, 'commentary/report_form.html', {'form': form})

