from django.db import models
from project.models import Project
from users.models import CustomUser


class Comment(models.Model):
    text=models.TextField()
    rate= models.IntegerField(default=0)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='comments')
    user =models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'


class Report(models.Model):
    reason = models.CharField(max_length=500)
    status = models.CharField(max_length=25)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reports')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reports')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reason
