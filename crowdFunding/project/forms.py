from django import forms
from project.models import Project,Tag,Category

class ProjectModelForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class TagModelForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'