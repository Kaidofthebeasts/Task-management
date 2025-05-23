# tasks/apps.py
from django.apps import AppConfig


class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'

    def ready(self):
        # Import signals here so they are registered when the app is ready
        import tasks.signals
