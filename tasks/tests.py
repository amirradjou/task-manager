# Import all test classes
from .test_models_views import TaskModelTest, TaskViewsTest
from .test_filtering_auth import TaskFilteringTest, AuthenticationTest
from .test_api import TaskAPITest, TaskAPIFilteringTest
from .test_serializers_forms import TaskSerializerTest, TaskFilterTest, CustomUserCreationFormTest

# Make all test classes available when running tests
__all__ = [
    'TaskModelTest',
    'TaskViewsTest', 
    'TaskFilteringTest',
    'AuthenticationTest',
    'TaskAPITest',
    'TaskAPIFilteringTest',
    'TaskSerializerTest',
    'TaskFilterTest',
    'CustomUserCreationFormTest',
]
