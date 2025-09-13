# Task Manager

A Django-based task management application with web interface and REST API.

## Features

- User authentication (signup/login)
- Create, edit, delete tasks
- Mark tasks as complete
- Search and filter tasks
- REST API with filtering and pagination
- User isolation (users only see their own tasks)

## Quick Start

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Start server: `python manage.py runserver`
7. Visit `http://127.0.0.1:8000/`

## API Usage

The REST API is available at `/api/tasks/` with authentication required.

```bash
# List tasks
curl -H "Authorization: Token your-token" http://127.0.0.1:8000/api/tasks/

# Create task
curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Token your-token" \
     -d '{"title": "New Task", "due_date": "2024-12-31"}' \
     http://127.0.0.1:8000/api/tasks/
```

## Testing

```bash
python manage.py test
```

## Tech Stack

- Django 5.2.6
- Django REST Framework
- SQLite
- django-filter