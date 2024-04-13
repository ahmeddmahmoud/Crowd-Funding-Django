from django.db import models
from project.models import Project
from users.models import CustomUser


class Comment(models.Model):
    text=models.TextField()
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='comments')
    user =models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'


