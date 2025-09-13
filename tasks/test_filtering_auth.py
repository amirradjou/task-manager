from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Task
from .forms import CustomUserCreationForm
from .serializes import TaskSerializer
from .filters import TaskFilter


class TaskFilteringTest(TestCase):
    """Test cases for task filtering and search"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test tasks
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
        
        self.task3 = Task.objects.create(
            title='Overdue Task',
            description='This task is overdue',
            due_date=date.today() - timedelta(days=2),
            completed=False,
            owner=self.user
        )
        
        self.client.login(username='testuser', password='testpass123')
    
    def test_search_functionality(self):
        """Test search functionality"""
        response = self.client.get(reverse('task_list'), {'search': 'important'})
        self.assertContains(response, 'Important Project')
        self.assertNotContains(response, 'Completed Task')
    
    def test_completed_filter(self):
        """Test completed status filter"""
        response = self.client.get(reverse('task_list'), {'completed': 'true'})
        self.assertContains(response, 'Completed Task')
        self.assertNotContains(response, 'Important Project')
    
    def test_incomplete_filter(self):
        """Test incomplete status filter"""
        response = self.client.get(reverse('task_list'), {'completed': 'false'})
        self.assertContains(response, 'Important Project')
        self.assertContains(response, 'Overdue Task')
        self.assertNotContains(response, 'Completed Task')
    
    def test_overdue_filter(self):
        """Test overdue filter"""
        response = self.client.get(reverse('task_list'), {'overdue': 'true'})
        self.assertContains(response, 'Overdue Task')
        self.assertNotContains(response, 'Important Project')
        self.assertNotContains(response, 'Completed Task')
    
    def test_ordering_by_due_date(self):
        """Test ordering by due date"""
        response = self.client.get(reverse('task_list'), {'ordering': 'due_date'})
        self.assertEqual(response.status_code, 200)
    
    def test_combined_filters(self):
        """Test combined filters"""
        response = self.client.get(reverse('task_list'), {
            'search': 'task',
            'completed': 'false'
        })
        self.assertContains(response, 'Important Project')
        self.assertContains(response, 'Overdue Task')
        self.assertNotContains(response, 'Completed Task')


class AuthenticationTest(TestCase):
    """Test cases for authentication"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_signup_view(self):
        """Test user signup"""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
    
    def test_signup_post(self):
        """Test user signup via POST"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after signup
        
        # Check user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_login_view(self):
        """Test login view"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_post(self):
        """Test login via POST"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after login
    
    def test_logout(self):
        """Test logout functionality"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout
