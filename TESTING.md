# Test Configuration for Task Manager

## Running Tests

### Run all tests:
```bash
python manage.py test
```

### Run specific test modules:
```bash
python manage.py test tasks.test_models_views
python manage.py test tasks.test_api
python manage.py test tasks.test_filtering_auth
python manage.py test tasks.test_serializers_forms
```

### Run specific test classes:
```bash
python manage.py test tasks.test_models_views.TaskModelTest
python manage.py test tasks.test_api.TaskAPITest
```

### Run specific test methods:
```bash
python manage.py test tasks.test_models_views.TaskModelTest.test_task_creation
```

### Run with coverage:
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generates HTML report in htmlcov/
```

## Test Structure

### Test Files:
- `test_models_views.py` - Tests for Task model and web views
- `test_filtering_auth.py` - Tests for filtering, search, and authentication
- `test_api.py` - Tests for REST API endpoints
- `test_serializers_forms.py` - Tests for serializers, filters, and forms
- `tests.py` - Main test file that imports all test classes

### Test Categories:

#### 1. Model Tests (`TaskModelTest`)
- Task creation and validation
- String representation
- Default values
- Owner relationships

#### 2. View Tests (`TaskViewsTest`)
- Authentication requirements
- User isolation (users only see their own tasks)
- CRUD operations
- Permission checks

#### 3. Filtering Tests (`TaskFilteringTest`)
- Search functionality
- Status filtering (completed/incomplete)
- Overdue task filtering
- Ordering and sorting
- Combined filters

#### 4. Authentication Tests (`AuthenticationTest`)
- User signup
- User login/logout
- Form validation

#### 5. API Tests (`TaskAPITest`, `TaskAPIFilteringTest`)
- API authentication requirements
- CRUD operations via API
- User isolation in API
- API filtering and search
- API ordering

#### 6. Serializer Tests (`TaskSerializerTest`)
- Data serialization
- Data validation
- Task creation via serializer

#### 7. Filter Tests (`TaskFilterTest`)
- Search filtering
- Status filtering
- Overdue filtering

#### 8. Form Tests (`CustomUserCreationFormTest`)
- Form validation
- Password confirmation
- User creation

## Test Coverage

The test suite covers:
- ✅ Model functionality and relationships
- ✅ Web dashboard views and permissions
- ✅ REST API endpoints and authentication
- ✅ Search and filtering functionality
- ✅ User authentication and authorization
- ✅ Form validation and user creation
- ✅ Data serialization and validation
- ✅ User isolation and security

## Test Data

Tests use:
- Test users with different permissions
- Sample tasks with various states (completed, overdue, etc.)
- Mock data for API testing
- Isolated test database (created and destroyed for each test run)

## Continuous Integration

For CI/CD pipelines, use:
```bash
python manage.py test --verbosity=2 --keepdb
```

This will:
- Run all tests with detailed output
- Keep the test database between runs for faster execution
- Exit with non-zero code if any tests fail
