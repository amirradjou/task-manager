# tasks/urls.py

from django.urls import path
from .views import SignUpView
# from .views import TaskListView

urlpatterns = [
    # The home page will be the task list
    # path('', TaskListView.as_view(), name='task_list'),
    path('signup/', SignUpView.as_view(), name='signup'),
]