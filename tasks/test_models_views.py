from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import date, timedelta
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import Task
from .forms import CustomUserCreationForm
from .serializes import TaskSerializer
from .filters import TaskFilter


class TaskModelTest(TestCase):
    """Test cases for the Task model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            due_date=date.today() + timedelta(days=1),
            owner=self.user
        )
    
    def test_task_creation(self):
        """Test task creation"""
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'This is a test task')
        self.assertEqual(self.task.owner, self.user)
        self.assertFalse(self.task.completed)
    
    def test_task_str_representation(self):
        """Test string representation of task"""
        self.assertEqual(str(self.task), 'Test Task')
    
    def test_task_default_completed_status(self):
        """Test that completed defaults to False"""
        new_task = Task.objects.create(
            title='New Task',
            due_date=date.today(),
            owner=self.user
        )
        self.assertFalse(new_task.completed)
    
    def test_task_owner_relationship(self):
        """Test task owner relationship"""
        self.assertEqual(self.task.owner, self.user)
        self.assertIn(self.task, self.user.task_set.all())


class TaskViewsTest(TestCase):
    """Test cases for task views"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            due_date=date.today() + timedelta(days=1),
            owner=self.user
        )
    
    def test_task_list_view_requires_login(self):
        """Test that task list view requires login"""
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_task_list_view_authenticated(self):
        """Test task list view for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')
    
    def test_task_list_view_user_isolation(self):
        """Test that users only see their own tasks"""
        # Create another user and task
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        Task.objects.create(
            title='Other Task',
            due_date=date.today(),
            owner=other_user
        )
        
        # Login as first user
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('task_list'))
        
        # Should only see own task
        self.assertContains(response, 'Test Task')
        self.assertNotContains(response, 'Other Task')
    
    def test_task_create_view_requires_login(self):
        """Test that task create view requires login"""
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 302)
    
    def test_task_create_view_authenticated(self):
        """Test task create view for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)
    
    def test_task_create_post(self):
        """Test creating a task via POST"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'New Task',
            'description': 'New task description',
            'due_date': date.today() + timedelta(days=7)
        }
        response = self.client.post(reverse('task_create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        
        # Check task was created
        new_task = Task.objects.get(title='New Task')
        self.assertEqual(new_task.owner, self.user)
    
    def test_task_update_view_user_isolation(self):
        """Test that users can only update their own tasks"""
        # Create another user and task
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        other_task = Task.objects.create(
            title='Other Task',
            due_date=date.today(),
            owner=other_user
        )
        
        # Login as first user and try to update other user's task
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('task_update', args=[other_task.pk]))
        self.assertEqual(response.status_code, 404)  # Should not be found
    
    def test_task_delete_view_user_isolation(self):
        """Test that users can only delete their own tasks"""
        # Create another user and task
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        other_task = Task.objects.create(
            title='Other Task',
            due_date=date.today(),
            owner=other_user
        )
        
        # Login as first user and try to delete other user's task
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('task_delete', args=[other_task.pk]))
        self.assertEqual(response.status_code, 404)  # Should not be found
