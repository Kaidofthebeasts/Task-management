# CLoud project/task_manager_project/context_processors.py
from tasks.models import Notification

def unread_notifications(request):
    """
    Adds the count of unread notifications for the logged-in user to the context.
    """
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'unread_notifications_count': unread_count}
    return {'unread_notifications_count': 0} # Return 0 if user is not authenticated
