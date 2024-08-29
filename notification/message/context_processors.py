from .models import Notification

def notifications_context(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(student__user=request.user, is_read=False)
        return {
            'notifications': notifications,
            'notifications_count': notifications.count(),
        }
    return {
        'notifications': [],
        'notifications_count': 0,
    }
