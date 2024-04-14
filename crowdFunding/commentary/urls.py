from django.urls import path
from commentary.views import add_comment, add_report


urlpatterns = [
    path('comment', add_comment, name='projects.comment'),
    path('report/<int:id>/', add_report, name='projects.report_project'),
    path('report/<int:id>/<int:comment_id>', add_report, name='projects.report_comment'),

]
