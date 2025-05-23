# tasks/models.py
from django.db import models
from django.contrib.auth import get_user_model # Use get_user_model for referencing the custom user model
from django.utils import timezone

User = get_user_model() # Get the currently active user model

class Category(models.Model):
    # A category now belongs to a user (one-to-many relationship)
    user = models.ForeignKey(
        User, # Use the User model obtained from get_user_model()
        on_delete=models.CASCADE, # If a user is deleted, their categories are also deleted
        related_name='categories', # Allows accessing categories from a user object (e.g., user.categories.all())
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True) # Added description back as it was in previous versions

    class Meta:
        verbose_name_plural = "Categories" # Fixes the plural name in Django Admin
        # Add a unique constraint for name and user to ensure a user cannot have two categories with the same name
        unique_together = ('user', 'name')

    def __str__(self):
        return f"{self.name} (by {self.user.username if self.user else 'Admin'})"


class Task(models.Model):
    PRIORITY_CHOICES = [ # Added PRIORITY_CHOICES back as it was in previous versions
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    # A task belongs to a user (one-to-many relationship)
    user = models.ForeignKey(
        User, # Use the User model obtained from get_user_model()
        on_delete=models.CASCADE, # If a user is deleted, their tasks are also deleted
        related_name='tasks' # Allows accessing tasks from a user object (e.g., user.tasks.all())
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    # A task can belong to a category (optional, many-to-one relationship)
    # Changed related_name from 'tasks' to 'category_tasks' to avoid clash
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, # If a category is deleted, tasks remain but lose their category
        blank=True,
        null=True,
        related_name='category_tasks'
    )
    due_date = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) # Added updated_at back as it was in previous versions
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium') # Added priority back

    # New field to track if a task has generated a notification for overdue/due soon
    # This helps prevent generating multiple notifications for the same event
    has_active_reminder_notification = models.BooleanField(default=False)


    class Meta:
        ordering = ['due_date', 'priority'] # Default ordering for tasks

    def __str__(self):
        return self.title

    # Properties for reminder logic (re-added as they were in previous versions)
    @property
    def is_overdue(self):
        return not self.completed and self.due_date and self.due_date < timezone.now()

    @property
    def is_due_soon(self):
        # A task is due soon if it's not completed, has a due date,
        # is not overdue, and is due within the next 7 days.
        now = timezone.now()
        seven_days_from_now = now + timezone.timedelta(days=7)
        return not self.completed and self.due_date and \
               not self.is_overdue and self.due_date <= seven_days_from_now


# NEW MODEL: Notification
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('overdue', 'Overdue Task'),
        ('due_soon', 'Task Due Soon'),
        ('general', 'General'), # For future use if you want other notification types
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    message = models.CharField(max_length=255)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='general')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # Order by most recent first

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"
