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
from .filters import TaskFilter


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
        from django.db.models import Q
        from django.utils import timezone
        
        # Start with user's tasks
        queryset = Task.objects.filter(owner=self.request.user)
        
        # Get filter parameters
        search = self.request.GET.get('search')
        completed = self.request.GET.get('completed')
        overdue = self.request.GET.get('overdue')
        ordering = self.request.GET.get('ordering')
        
        # Apply search filter
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search)
            )
        
        # Apply completion status filter
        if completed == 'true':
            queryset = queryset.filter(completed=True)
        elif completed == 'false':
            queryset = queryset.filter(completed=False)
        
        # Apply overdue filter
        if overdue == 'true':
            queryset = queryset.filter(
                due_date__lt=timezone.now().date(),
                completed=False
            )
        
        # Apply ordering
        if ordering:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by('due_date')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.utils import timezone
        
        # Get all user's tasks for stats (not filtered)
        all_tasks = Task.objects.filter(owner=self.request.user)
        
        # Calculate stats
        context['total_tasks'] = all_tasks.count()
        context['completed_tasks'] = all_tasks.filter(completed=True).count()
        context['incomplete_tasks'] = all_tasks.filter(completed=False).count()
        context['overdue_tasks'] = all_tasks.filter(
            due_date__lt=timezone.now().date(),
            completed=False
        ).count()
        context['today'] = timezone.now().date()
        
        return context

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
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'title', 'created_at']
    ordering = ['due_date']

    def get_queryset(self):
        # Ensure users can only see and manage their own tasks
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the logged-in user as the owner
        serializer.save(owner=self.request.user)