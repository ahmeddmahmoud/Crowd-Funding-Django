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
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 3:
            raise forms.ValidationError('Title length must be greater then 3 characters')
        return title
    
    def clean_total_target(self):
        total_target = self.cleaned_data['total_target']
        if total_target <= 5000:
            raise forms.ValidationError("Total target must be grater than 5000.")
        return total_target
    
    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        if start_date < datetime.now().date():
            raise forms.ValidationError('Start date must be greater than today')
        return start_date


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.isalpha():
            raise forms.ValidationError('Category name must be alphabetic')
        if name is None or len(name) < 3:
            raise forms.ValidationError('Category name should be at least 3 characters')
        return name


class TagModelForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.isalpha():
            raise forms.ValidationError('Tag name must be alphabetic')
        if name is None or len(name) < 3:
            raise forms.ValidationError('Tag name should be at least 3 characters')
        return name


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
        fields = ['image']
        
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError("You must upload an image.")
        return image

