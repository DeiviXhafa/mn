from django.urls import path
from .views import *
urlpatterns=[
    path('taskview/',TaskView.as_view()),
    path('task/add/<id>/',AddProjectTaskView.as_view()),
    path('task/view/<id>',TaskIDView.as_view()),
    path('task/add/',AddTaskView.as_view()),
    path('project/',ProjectView.as_view()),
    path('project/<id>',ProjectTaskView.as_view()),
    path('subtask/view/<id>',SubTaskIDView.as_view()),
    path('subtask/<task_id>',SubTaskView.as_view()),
    path('subtask/add/<id>',AddSubTaskView.as_view()),
    path('subtask/edit/<id>',EditSubTaskView.as_view()),
    path('<model>/',ReadView.as_view()),
    path('<model>/add',AddView.as_view()),


]
