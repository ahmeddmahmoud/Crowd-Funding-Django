from django import forms
from project.models import Project,Tag,Category,Donation,Picture
from datetime import datetime
from django.utils import timezone

class ProjectModelForm(forms.ModelForm):    
    class Meta:
        model = Project
        fields = ('title', 'details', 'total_target', 'start_date', 'end_date','category', 'tag')
        
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date <= start_date:
                raise forms.ValidationError('End date must be greater than start date')

        return cleaned_data


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

        def clean_name(self):
            name = self.cleaned_data.get('name')
            if name is None or len(name) < 3:
                raise forms.ValidationError('Name must be provided and have a length greater than 3 characters')
            return name


class TagModelForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'


class DonationModelForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ('donation',)
        
    def clean_donation(self):
        donation = self.cleaned_data['donation']
        if donation <= 0:
            raise forms.ValidationError("Donation amount must be positive.")
        return donation
        
    
    
    
class PictureModelForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ('image',)
    

