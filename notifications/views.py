from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.db.models.functions import TruncMinute
from notifications.models import Message, Notification


# Create your views here.

class NotificationsView(LoginRequiredMixin,TemplateView):
    login_url = 'login'
    template_name = 'notifications/notifications.html'

    def get(self, request, *args, **kwargs):
        notifications = Message.objects.filter(
            notification__user=request.user  # Filter messages where the related notification's user is the current user
        ).select_related(
            'notification'  # Include related notification objects in the same query to avoid additional queries
        ).annotate(
            truncated_notification_date=TruncMinute('notification_date')  # Truncate notification_date to the nearest minute
        ).order_by(
            '-notification_date'  # Order the results by notification_date in descending order
        )

        return render(request, self.template_name, {
                    'notifications': notifications,
                })