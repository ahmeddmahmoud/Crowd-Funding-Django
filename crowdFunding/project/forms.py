from django import forms
from project.models import Project,Tag,Category,Donation,Picture


class ProjectModelForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'details', 'total_target', 'start_date', 'end_date','category', 'tag')


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class TagModelForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'


class DonationModelForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ('donation',)
        
class PictureModelForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ('image',)
    

