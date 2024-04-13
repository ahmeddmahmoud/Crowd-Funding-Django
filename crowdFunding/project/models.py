from django.db import models
from django.shortcuts import get_object_or_404 , reverse
from django.utils import timezone
from users.models import CustomUser


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f"{self.name}"

class Tag(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name



class Project(models.Model):
    title = models.CharField(max_length=200, unique=True)
    details = models.TextField(default="No details")
    total_target = models.FloatField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    current_donation = models.FloatField(default=0, null=True, blank=True)
    owner=models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    tag = models.ManyToManyField(Tag, blank=True, related_name="projects")

    def __str__(self):
        return self.title
    @property
    def show_url(self):
        url = reverse('project.show', args=[self.id])
        return url


class Picture(models.Model):
    image = models.ImageField(upload_to='project/images/', null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE , related_name='images')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"/media/{self.image}"

class Donation(models.Model):
    donation=models.FloatField()
    project=models.ForeignKey(Project, on_delete=models.CASCADE, related_name='donations')
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.donation



