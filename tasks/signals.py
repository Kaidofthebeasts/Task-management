# tasks/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.mail import send_mail # Import send_mail
from django.template.loader import render_to_string # To render email templates
from django.conf import settings # To access EMAIL_HOST_USER

from .models import Task, Notification

@receiver(post_save, sender=Task)
def create_deadline_notification(sender, instance, created, **kwargs):
    """
    Creates or updates notifications (in-app and email) for overdue or soon-due tasks.
    Prevents duplicate notifications for the same event.
    """
    # Only consider tasks that are not completed
    if not instance.completed:
        # Check if task is overdue
        if instance.is_overdue and not instance.has_active_reminder_notification:
            # Create an overdue notification if one doesn't exist and task is overdue
            Notification.objects.create(
                user=instance.user,
                task=instance,
                message=f"Task '{instance.title}' is overdue!",
                notification_type='overdue',
                is_read=False
            )
            instance.has_active_reminder_notification = True
            instance.save(update_fields=['has_active_reminder_notification']) # Save without re-triggering signal
            print(f"Notification created: Task '{instance.title}' is overdue.")

            # --- Send Email Notification for Overdue Task ---
            if instance.user.email: # Ensure the user has an email address
                subject = f"OVERDUE: Your Task '{instance.title}'"
                # You can create a dedicated HTML template for the email later
                message = (
                    f"Hello {instance.user.username},\n\n"
                    f"Your task '{instance.title}' was due on {instance.due_date.strftime('%Y-%m-%d %H:%M')}, but it is still pending.\n\n"
                    f"Description: {instance.description or 'N/A'}\n"
                    f"Category: {instance.category.name if instance.category else 'N/A'}\n\n"
                    f"Please log in to your Task Manager to update its status: {settings.BASE_URL if hasattr(settings, 'BASE_URL') else 'http://127.0.0.1:8000'}\n\n"
                    f"Thank you,\nYour Task Manager"
                )
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [instance.user.email]

                try:
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                    print(f"Email sent for overdue task '{instance.title}' to {instance.user.email}")
                except Exception as e:
                    print(f"Error sending email for overdue task '{instance.title}': {e}")


        # Check if task is due soon (and not already overdue, handled by is_due_soon property)
        elif instance.is_due_soon and not instance.has_active_reminder_notification:
            # Create a 'due soon' notification if one doesn't exist and task is due soon
            Notification.objects.create(
                user=instance.user,
                task=instance,
                message=f"Task '{instance.title}' is due soon!",
                notification_type='due_soon',
                is_read=False
            )
            instance.has_active_reminder_notification = True
            instance.save(update_fields=['has_active_reminder_notification']) # Save without re-triggering signal
            print(f"Notification created: Task '{instance.title}' is due soon.")

            # --- Send Email Notification for Due Soon Task ---
            if instance.user.email: # Ensure the user has an email address
                subject = f"REMINDER: Your Task '{instance.title}' is due soon!"
                message = (
                    f"Hello {instance.user.username},\n\n"
                    f"Just a friendly reminder that your task '{instance.title}' is due on {instance.due_date.strftime('%Y-%m-%d %H:%M')}.\n\n"
                    f"Description: {instance.description or 'N/A'}\n"
                    f"Category: {instance.category.name if instance.category else 'N/A'}\n\n"
                    f"Please log in to your Task Manager to review or complete it: {settings.BASE_URL if hasattr(settings, 'BASE_URL') else 'http://127.0.0.1:8000'}\n\n"
                    f"Thank you,\nYour Task Manager"
                )
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [instance.user.email]

                try:
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                    print(f"Email sent for due soon task '{instance.title}' to {instance.user.email}")
                except Exception as e:
                    print(f"Error sending email for due soon task '{instance.title}': {e}")


    # If a task is completed, or its due date is changed such that it's no longer overdue/due soon,
    # reset the has_active_reminder_notification flag and mark notifications as read.
    # Note: We don't send emails here, as the condition is resolved.
    if instance.completed or (not instance.is_overdue and not instance.is_due_soon and instance.has_active_reminder_notification):
        if instance.has_active_reminder_notification:
            # Mark associated in-app notifications as read
            Notification.objects.filter(task=instance, is_read=False).update(is_read=True)
            instance.has_active_reminder_notification = False
            instance.save(update_fields=['has_active_reminder_notification'])
            print(f"Active reminder notification for task '{instance.title}' reset and in-app notifications marked read.")

