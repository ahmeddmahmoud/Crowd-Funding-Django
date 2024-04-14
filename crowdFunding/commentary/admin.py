from django.contrib import admin

# Register your models here.
from commentary.models import Comment, Report

admin.site.register(Comment)
admin.site.register(Report)
