from django.db import models
from project.models import Project 
from users.models import User


class Comment(models.Model):
    content=models.CharField(max_length=500)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='comments')
    user =models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'
