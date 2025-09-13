from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date, timedelta

from .models import Task
from .forms import CustomUserCreationForm
from .serializes import TaskSerializer
from .filters import TaskFilter


class TaskSerializerTest(TestCase):
    """Test cases for Task serializer"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.task = Task.objects.create(
            title='Serializer Test Task',
            description='This is a test task for serializer',
            due_date=date.today() + timedelta(days=1),
            completed=False,
            owner=self.user
        )
    
    def test_task_serializer(self):
        """Test Task serializer"""
        serializer = TaskSerializer(self.task)
        expected_data = {
            'id': self.task.id,
            'title': 'Serializer Test Task',
            'description': 'This is a test task for serializer',
            'due_date': str(self.task.due_date),  # Convert to string for comparison
            'completed': False
        }
        self.assertEqual(serializer.data, expected_data)
    
    def test_task_serializer_create(self):
        """Test Task serializer create"""
        data = {
            'title': 'New Serializer Task',
            'description': 'New task via serializer',
            'due_date': date.today() + timedelta(days=7),
            'completed': False
        }
        serializer = TaskSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        task = serializer.save(owner=self.user)
        self.assertEqual(task.title, 'New Serializer Task')
        self.assertEqual(task.owner, self.user)


class TaskFilterTest(TestCase):
    """Test cases for Task filter"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.task1 = Task.objects.create(
            title='Important Project',
            description='This is an important project task',
            due_date=date.today() + timedelta(days=1),
            completed=False,
            owner=self.user
        )
        
        self.task2 = Task.objects.create(
            title='Completed Task',
            description='This task is done',
            due_date=date.today() - timedelta(days=1),
            completed=True,
            owner=self.user
        )
    
    def test_task_filter_search(self):
        """Test Task filter search functionality"""
        queryset = Task.objects.filter(owner=self.user)
        filter_data = {'search': 'important'}
        filtered_queryset = TaskFilter(filter_data, queryset=queryset).qs
        self.assertEqual(filtered_queryset.count(), 1)
        self.assertEqual(filtered_queryset.first(), self.task1)
    
    def test_task_filter_completed(self):
        """Test Task filter completed status"""
        queryset = Task.objects.filter(owner=self.user)
        filter_data = {'completed': 'true'}
        filtered_queryset = TaskFilter(filter_data, queryset=queryset).qs
        self.assertEqual(filtered_queryset.count(), 1)
        self.assertEqual(filtered_queryset.first(), self.task2)
    
    def test_task_filter_overdue(self):
        """Test Task filter overdue functionality"""
        queryset = Task.objects.filter(owner=self.user)
        filter_data = {'overdue': 'true'}
        filtered_queryset = TaskFilter(filter_data, queryset=queryset).qs
        # Should return completed task since it's overdue but not completed
        self.assertEqual(filtered_queryset.count(), 0)


class CustomUserCreationFormTest(TestCase):
    """Test cases for CustomUserCreationForm"""
    
    def test_form_valid_data(self):
        """Test form with valid data"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_invalid_password_mismatch(self):
        """Test form with password mismatch"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'differentpass'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_form_save(self):
        """Test form save functionality"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'newuser@example.com')
