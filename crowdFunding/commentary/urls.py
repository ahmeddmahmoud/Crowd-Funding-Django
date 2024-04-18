from django.urls import path
from commentary.views import add_comment, add_report, create_reply
from . import views
urlpatterns = [
    path('<int:id>/comment', views.add_comment, name='project.comment'),
    path('report/<int:id>/', add_report, name='projects.report_project'),
    path('report/<int:id>/<int:comment_id>', add_report, name='projects.report_comment'),
    # path('<int:comment_id>/reply', create_reply, name='projects.reply'),
    path('<int:project_id>/reply/<int:comment_id>', create_reply, name='projects.reply'),

]
