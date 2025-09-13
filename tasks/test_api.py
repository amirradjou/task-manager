from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date, timedelta
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Task
from .forms import CustomUserCreationForm
from .serializes import TaskSerializer
from .filters import TaskFilter


class TaskAPITest(APITestCase):
    """Test cases for Task API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.task = Task.objects.create(
            title='API Test Task',
            description='This is a test task for API',
            due_date=date.today() + timedelta(days=1),
            owner=self.user
        )
    
    def test_api_task_list_requires_authentication(self):
        """Test that API task list requires authentication"""
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_api_task_list_authenticated(self):
        """Test API task list for authenticated user"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'API Test Task')
    
    def test_api_task_create(self):
        """Test creating a task via API"""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New API Task',
            'description': 'New task created via API',
            'due_date': date.today() + timedelta(days=7)
        }
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check task was created
        new_task = Task.objects.get(title='New API Task')
        self.assertEqual(new_task.owner, self.user)
    
    def test_api_task_update(self):
        """Test updating a task via API"""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Updated API Task',
            'description': 'Updated task description',
            'due_date': date.today() + timedelta(days=2),
            'completed': True
        }
        response = self.client.put(f'/api/tasks/{self.task.pk}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check task was updated
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated API Task')
        self.assertTrue(self.task.completed)
    
    def test_api_task_delete(self):
        """Test deleting a task via API"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/tasks/{self.task.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check task was deleted
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
    
    def test_api_user_isolation(self):
        """Test that users can only access their own tasks via API"""
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
        
        # Login as first user and try to access other user's task
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/tasks/{other_task.pk}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TaskAPIFilteringTest(APITestCase):
    """Test cases for API filtering and search"""
    
    def setUp(self):
        """Set up test data"""
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
        
        self.client.force_authenticate(user=self.user)
    
    def test_api_search(self):
        """Test API search functionality"""
        response = self.client.get('/api/tasks/', {'search': 'important'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Important Project')
    
    def test_api_completed_filter(self):
        """Test API completed status filter"""
        response = self.client.get('/api/tasks/', {'completed': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Completed Task')
    
    def test_api_overdue_filter(self):
        """Test API overdue filter"""
        response = self.client.get('/api/tasks/', {'overdue': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Overdue Task')
    
    def test_api_ordering(self):
        """Test API ordering"""
        response = self.client.get('/api/tasks/', {'ordering': 'due_date'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
