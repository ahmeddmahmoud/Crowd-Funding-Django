from django import forms
from commentary.models import Comment, Report, Reply

class CommentForm(forms.ModelForm):
    rate = forms.IntegerField(label='Rating', min_value=1, max_value=5, initial=0)  # Add a rating field
    class Meta:
        model = Comment
        fields = ['text','rate']



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



class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']