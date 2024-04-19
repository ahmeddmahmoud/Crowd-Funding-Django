from django import forms
from commentary.models import Comment, Report, Reply
from django.core.exceptions import ValidationError


class CommentForm(forms.ModelForm):
    rate = forms.IntegerField(label='Rating', min_value=1, max_value=5, initial=0)  # Add a rating field
    class Meta:
        model = Comment
        fields = ['text','rate']

    def clean_rate(self):
        rate=self.cleaned_data['rate']
        if rate < 0 or rate > 5:
            raise ValidationError("Rate must be between 0 and 5")
        return rate

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if text is None or len(text) < 3:
            raise forms.ValidationError('text must be provided and have a length greater than 3 characters')
        return text



class ReportForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('Hateful Speech', 'Hateful Speech'),
        ('Terrorism', 'Terrorism'),
        ('Abuse', 'Abuse'),
        ('Violence', 'Violence'),
        ('Irrelevant', 'Irrelevant')
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = Report
        fields = ['reason', 'status']

    def clean_reason(self):
        reason = self.cleaned_data.get('reason')
        if reason is None or len(reason) < 3:
            raise forms.ValidationError('reason must be provided and have a length greater than 3 characters')
        return reason


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError('Content must be provided.')
        elif len(content) < 3:
            raise forms.ValidationError('Content must have a length greater than 3 characters.')
        return content

