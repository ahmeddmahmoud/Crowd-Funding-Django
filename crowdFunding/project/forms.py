from django import forms
from project.models import Project

class ProjectModelForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
