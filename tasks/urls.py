# tasks/urls.py

from django.urls import path
from .views import (
    SignUpView,
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView
)
urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('task/create/', TaskCreateView.as_view(), name='task_create'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]