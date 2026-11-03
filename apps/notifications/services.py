"""
Services for the notifications application.
"""
from .models import Notification, NotificationTemplate, NotificationPreference


class NotificationService:
    """
    Service for notification operations.
    """
    
    def __init__(self, request):
        self.request = request
        self.user = request.user
    
    def create_notification(self, data):
        """
        Create a new notification.
        """
        notification = Notification.objects.create(
            notification_type=data.get('notification_type'),
            user_id=data.get('user_id'),
            title=data.get('title'),
            message=data.get('message'),
            entity_type=data.get('entity_type'),
            entity_id=data.get('entity_id'),
            entity_url=data.get('entity_url'),
            organization_id=data.get('organization_id'),
            branch_id=data.get('branch_id'),
            priority=data.get('priority', 'medium'),
            delivery_method=data.get('delivery_method', 'in_app'),
            actions=data.get('actions', [])
        )
        
        return self.get_notification_data(notification)
    
    def send_notification(self, notification_type, user, title, message, **kwargs):
        """
        Send a notification to a user.
        """
        notification = Notification.objects.create(
            notification_type=notification_type,
            user=user,
            title=title,
            message=message,
            entity_type=kwargs.get('entity_type'),
            entity_id=kwargs.get('entity_id'),
            entity_url=kwargs.get('entity_url'),
            organization=kwargs.get('organization'),
            branch=kwargs.get('branch'),
            priority=kwargs.get('priority', 'medium'),
            delivery_method=kwargs.get('delivery_method', 'in_app'),
            actions=kwargs.get('actions', [])
        )
        
        # In a real implementation, we would also send email/SMS here
        
        return self.get_notification_data(notification)
    
    def mark_notification_as_read(self, pk):
        """
        Mark a notification as read.
        """
        try:
            notification = Notification.objects.get(pk=pk, user=self.user)
            notification.mark_as_read()
            return self.get_notification_data(notification)
        except Notification.DoesNotExist:
            return None
    
    def mark_all_notifications_as_read(self):
        """
        Mark all notifications as read.
        """
        count = Notification.objects.filter(
            user=self.user,
            is_read=False
        ).update(is_read=True)
        
        return count
    
    def delete_notification(self, pk):
        """
        Delete a notification.
        """
        try:
            notification = Notification.objects.get(pk=pk, user=self.user)
            notification.delete()
            return True
        except Notification.DoesNotExist:
            return False
    
    def archive_notification(self, pk):
        """
        Archive a notification.
        """
        try:
            notification = Notification.objects.get(pk=pk, user=self.user)
            notification.mark_as_archived()
            return True
        except Notification.DoesNotExist:
            return False
    
    def get_notification_data(self, notification):
        """
        Get notification data for API responses.
        """
        return {
            'id': str(notification.id),
            'notification_type': notification.notification_type,
            'notification_type_display': notification.get_notification_type_display(),
            'user': {
                'id': str(notification.user.id),
                'email': notification.user.email,
                'username': notification.user.username,
            },
            'title': notification.title,
            'message': notification.message,
            'entity_type': notification.entity_type,
            'entity_id': str(notification.entity_id) if notification.entity_id else None,
            'entity_url': notification.entity_url,
            'organization': {
                'id': str(notification.organization.id) if notification.organization else None,
                'name': notification.organization.name if notification.organization else None,
            } if notification.organization else None,
            'branch': {
                'id': str(notification.branch.id) if notification.branch else None,
                'name': notification.branch.name if notification.branch else None,
            } if notification.branch else None,
            'is_read': notification.is_read,
            'is_archived': notification.is_archived,
            'priority': notification.priority,
            'priority_display': notification.get_priority_display(),
            'delivery_method': notification.delivery_method,
            'is_delivered': notification.is_delivered,
            'delivered_at': notification.delivered_at.isoformat() if notification.delivered_at else None,
            'actions': notification.actions,
            'created_at': notification.created_at.isoformat(),
        }
