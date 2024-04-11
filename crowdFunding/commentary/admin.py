from django.contrib import admin

# Register your models here.
from commentary.models import Comment

admin.site.register(Comment)