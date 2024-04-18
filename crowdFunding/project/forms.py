from django import forms
from project.models import Project,Tag,Category,Donation


class ProjectModelForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'details', 'total_target', 'start_date', 'end_date','category', 'tag')


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


