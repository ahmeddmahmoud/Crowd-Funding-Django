from django.db import models
from django.shortcuts import get_object_or_404 , reverse
from django.utils import timezone
from users.models import User



# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f"{self.name}"

    @classmethod
    def get_category_by_id(cls, id):
        return get_object_or_404(cls,pk=id)

    @property
    def delete_url(self):
        url=reverse ("category.delete",args=[self.id])
        return url

    @property
    def show_url(self):
        url=reverse("category.show",args=[self.id])
        return url

    @property
    def edit_url(self):
        return reverse("category.edit",args=[self.id])


class Tag(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_tag_by_id(cls, id):
        return get_object_or_404(cls, pk=id)

    @property
    def delete_url(self):
        url = reverse("tag.delete", args=[self.id])
        return url

    # @property
    # def show_url(self):
    #     url = reverse("tag.show", args=[self.id])
    #     return url

    @property
    def edit_url(self):
        return reverse("tag.edit", args=[self.id])



class Project(models.Model):
    title = models.CharField(max_length=200, unique=True)
    details = models.TextField(default="No details")
    total_target = models.FloatField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    current_donation = models.FloatField(default=0, null=True, blank=True)
    project_owner=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    featured_at = models.DateTimeField(default=None, null=True, blank=True)
    category= models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    tag = models.ManyToManyField(Tag, blank=True, related_name="projects")

    def __str__(self):
        return self.title
    @property
    def show_url(self):
        url = reverse('project.show', args=[self.id])
        return url

    @property
    def edit_url(self):
        url = reverse('project.edit', args=[self.id])
        return url

    @classmethod

    def get_project_by_id(cls,id):
        return get_object_or_404(cls, pk=id)

    
    @property
    def delete_url(self):
        url = reverse('project.cancel', args=[self.id])
        return url
    
    @property
    def rate(self):
        comments = self.comments.all()
        if comments.exists():
            return round(sum(comment.rate for comment in comments) / len(comments), 1)
        return 0

    @property
    def star_ratings(self):
        rate = self.rate
        return [1 if i < rate else 0.5 if abs(i - rate) <= 0.5 else 0 for i in range(1, 6)]
    @property
    def donate_url(self):
        url = reverse('project.donate', args=[self.id])
        return url

    def featured_project(self):
        if not self.is_featured:
            self.is_featured=True
            self.featured_at=timezone.now()
            self.save()

    def not_featured_project(self):
        if self.is_featured:
            self.is_featured=False
            self.featured_at=None
            self.save()


class Picture(models.Model):
    image = models.ImageField(upload_to='project/images/', null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE , related_name='images')

    def __str__(self):
        return f"/media/{self.image}"

class Donation(models.Model):
    donation=models.FloatField()
    project=models.ForeignKey(Project, on_delete=models.CASCADE, related_name='donations')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.donation



