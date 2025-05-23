# tasks/scripts/populate_tasks.py

from accounts.models import CustomUser
from tasks.models import Category, Task
from django.utils import timezone
import os
import sys

def run():
    print("--- Starting Data Population ---")

    username_to_populate = 'test' 
    try:
        user = CustomUser.objects.get(username=username_to_populate)
        print(f"Populating data for user: {user.username}")
    except CustomUser.DoesNotExist:
        print(f"Error: User '{username_to_populate}' not found.")
        print("Please ensure this user exists or change 'username_to_populate' in the script.")
        sys.exit(1)

    # 1. Create Sample Categories for the specific user
    print("\nCreating Categories...")
    categories_to_create = [
        {'name': 'Work', 'description': 'Tasks related to professional duties.'},
        {'name': 'Personal', 'description': 'Tasks for personal life and errands.'},
        {'name': 'Shopping', 'description': 'Items to buy.'},
        {'name': 'Health', 'description': 'Fitness and wellness related tasks.'},
        {'name': 'Learning', 'description': 'Educational activities.'},
    ]

    created_categories = {}
    for cat_data in categories_to_create:
        # Assign the user to the category being created or retrieved
        category, created = Category.objects.get_or_create(
            user=user, # Assign the user here
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        created_categories[category.name] = category
        if created:
            print(f" - Created category: {category.name} for user {user.username}")
        else:
            print(f" - Category '{category.name}' already exists for user {user.username}. Skipping.")

    # 2. Create Sample Tasks for the User
    print("\nCreating Tasks...")
    tasks_to_create = [
        {
            'title': 'Finish Django Project',
            'description': 'Complete the task management app backend and frontend.',
            'category_name': 'Work',
            'due_date_offset_days': 7,
            'completed': False
        },
        {
            'title': 'Buy Groceries',
            'description': 'Milk, Eggs, Bread, Vegetables.',
            'category_name': 'Shopping',
            'due_date_offset_days': 2,
            'completed': False
        },
        {
            'title': 'Call Mom',
            'description': 'Check in and say hello.',
            'category_name': 'Personal',
            'due_date_offset_days': 1,
            'completed': False
        },
        {
            'title': 'Go for a run',
            'description': '30-minute outdoor run.',
            'category_name': 'Health',
            'due_date_offset_days': 0, # Due today
            'completed': False
        },
        {
            'title': 'Read Django Docs',
            'description': 'Review authentication and generic views documentation.',
            'category_name': 'Work',
            'due_date_offset_days': 10,
            'completed': False
        },
        {
            'title': 'Pay Bills',
            'description': 'Electricity and Internet bills due this week.',
            'category_name': 'Personal',
            'due_date_offset_days': -3, # Overdue task
            'completed': False
        },
        {
            'title': 'Schedule Dentist Appointment',
            'description': 'Annual checkup.',
            'category_name': 'Health',
            'due_date_offset_days': 14,
            'completed': False
        },
        {
            'title': 'Plan Weekend Trip',
            'description': 'Research destinations and book accommodation.',
            'category_name': 'Personal',
            'due_date_offset_days': 20,
            'completed': False
        },
        {
            'title': 'Write Blog Post',
            'description': 'Draft content for the new tech blog.',
            'category_name': 'Work',
            'due_date_offset_days': 5,
            'completed': True # Example of a completed task
        },
        {
            'title': 'Learn Python Basics',
            'description': 'Review Python syntax and data structures.',
            'category_name': 'Learning',
            'due_date_offset_days': 15,
            'completed': False
        },
        {
            'title': 'Prepare for Meeting',
            'description': 'Review agenda and prepare presentation slides.',
            'category_name': 'Work',
            'due_date_offset_days': -1, # Overdue task
            'completed': False
        },
    ]

    for task_data in tasks_to_create:
        category = created_categories.get(task_data['category_name'])
        due_date = None
        if task_data['due_date_offset_days'] is not None:
            due_date = timezone.now() + timezone.timedelta(days=task_data['due_date_offset_days'])

        # Check if a task with the same title already exists for this user
        task_exists = Task.objects.filter(user=user, title=task_data['title']).exists()

        if not task_exists:
            Task.objects.create(
                user=user,
                title=task_data['title'],
                description=task_data['description'],
                category=category,
                due_date=due_date,
                completed=task_data['completed']
            )
            print(f" - Created task: '{task_data['title']}' for user '{user.username}'")
        else:
            print(f" - Task '{task_data['title']}' already exists for user '{user.username}'. Skipping.")

    print("\n--- Data Population Complete ---")
