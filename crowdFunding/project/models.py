from django.db import models
from django.shortcuts import get_object_or_404 , reverse
from django.utils import timezone

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f"{self.name}"


class Project(models.Model):
    title = models.CharField(max_length=200, unique=True)
    details = models.TextField(default="No details")
    total_target = models.FloatField()
    start_date = models.DateField(default=timezone.now().date())
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    current_donation = models.FloatField(default=0, null=True)
    
    def __str__(self):
        return self.title


# class Picture(models.Model):
#     image = models.ImageField(upload_to='project/images/' , null=True)
#     # project = models.ForeignKey(Project, on_delete=models.CASCADE , related_name='images')
#
#     def __str__(self):
#         return f"/media/{self.image}"



