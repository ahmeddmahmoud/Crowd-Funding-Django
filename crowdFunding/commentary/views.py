from django.shortcuts import render, redirect, get_object_or_404
from .forms import CommentForm, ReportForm, ReplyForm
from .models import Project, Comment, Reply
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def add_comment(request, id):
    project = get_object_or_404(Project, pk=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.user = request.user
            comment.save()

            # Handle stars rating data
            star_rating = request.POST.get('star_rating')
            print("Star Rating:", star_rating)  # Debugging statement
            if star_rating:
                comment.star_rating = int(star_rating)
                comment.save()
            print("Comment:", comment)
            return redirect('project.show', id=id)
        else:
            messages.error(request,"comment can't be empty")
            return redirect('project.show',id=id)
    else:
        form = CommentForm()
    return render(request, 'project/crud/show.html', {'form': form})

# Create your views here.


@login_required
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




@login_required
def create_reply(request,project_id,comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    project=get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comment
            reply.user = request.user
            reply.save()
            print(project_id )
            return redirect('project.show', id=project_id)
        else:
            messages.error(request,"reply can't be empty")
            return redirect('project.show', id=project_id)

    else:
        form = ReplyForm()

    # return redirect('products.show', id=comment.product.id)  # Redirect even for GET request
    return render(request, 'project/crud/show.html', {'form': form})
