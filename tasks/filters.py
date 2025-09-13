import django_filters
from django.db.models import Q
from .models import Task


class TaskFilter(django_filters.FilterSet):
    # Search filter for title and description
    search = django_filters.CharFilter(method='filter_search', label='Search')
    
    # Filter by completion status
    completed = django_filters.BooleanFilter(field_name='completed')
    
    # Filter by due date range
    due_date_from = django_filters.DateFilter(field_name='due_date', lookup_expr='gte', label='Due date from')
    due_date_to = django_filters.DateFilter(field_name='due_date', lookup_expr='lte', label='Due date to')
    
    # Filter by overdue tasks (past due date and not completed)
    overdue = django_filters.BooleanFilter(method='filter_overdue', label='Overdue')
    
    # Ordering
    ordering = django_filters.OrderingFilter(
        fields=(
            ('due_date', 'due_date'),
            ('title', 'title'),
            ('created_at', 'created_at'),
        ),
        field_labels={
            'due_date': 'Due Date',
            'title': 'Title',
            'created_at': 'Created Date',
        }
    )

    class Meta:
        model = Task
        fields = ['completed', 'due_date_from', 'due_date_to', 'overdue']

    def filter_search(self, queryset, name, value):
        """
        Search in title and description fields
        """
        if value:
            return queryset.filter(
                Q(title__icontains=value) | 
                Q(description__icontains=value)
            )
        return queryset

    def filter_overdue(self, queryset, name, value):
        """
        Filter for overdue tasks (past due date and not completed)
        """
        from django.utils import timezone
        
        if value:
            return queryset.filter(
                due_date__lt=timezone.now().date(),
                completed=False
            )
        return queryset
