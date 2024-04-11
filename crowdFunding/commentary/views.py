from django.shortcuts import render, redirect, get_object_or_404

from .models import Project, Comment
from .forms import CommentForm

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
            return redirect('hello',id=id)
    else:
        form = CommentForm()
        return render(request, 'test.html', {'form': form})




