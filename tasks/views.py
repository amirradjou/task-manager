# tasks/views.py

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .forms import CustomUserCreationForm
from .serializes import TaskSerializer


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# --- Add the new views below ---

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        # This is the most important part: filter tasks by the current logged-in user.
        return Task.objects.filter(owner=self.request.user)

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'due_date'] # Fields the user can fill out
    template_name = 'task/task_form.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        # Before saving the form, set the owner to the current user.
        form.instance.owner = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'completed'] # Allow updating the completed status
    template_name = 'task/task_form.html'
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        # Ensure the user can only update their own tasks.
        return Task.objects.filter(owner=self.request.user)

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        # Ensure the user can only delete their own tasks.
        return Task.objects.filter(owner=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure users can only see and manage their own tasks
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the logged-in user as the owner
        serializer.save(owner=self.request.user)