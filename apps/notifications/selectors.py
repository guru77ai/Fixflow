"""
Selectors for the notifications application.
"""
from django.db.models import Q
from .models import Notification, NotificationTemplate, NotificationPreference


class NotificationSelector:
    """
    Selector for notification queries.
    """
    
    def __init__(self, request):
        self.request = request
        self.user = request.user
    
    def get_notification(self, pk):
        """
        Get a notification by ID.
        """
        try:
            notification = Notification.objects.get(pk=pk, user=self.user)
            return self.get_notification_data(notification)
        except Notification.DoesNotExist:
            return None
    
    def get_notifications(self, **filters):
        """
        Get a list of notifications.
        """
        queryset = Notification.objects.filter(user=self.user)
        
        # Apply filters
        if 'is_read' in filters:
            queryset = queryset.filter(is_read=filters['is_read'])
        
        if 'is_archived' in filters:
            queryset = queryset.filter(is_archived=filters['is_archived'])
        
        if 'notification_type' in filters:
            queryset = queryset.filter(notification_type=filters['notification_type'])
        
        if 'priority' in filters:
            queryset = queryset.filter(priority=filters['priority'])
        
        if 'start_date' in filters:
            queryset = queryset.filter(created_at__gte=filters['start_date'])
        
        if 'end_date' in filters:
            queryset = queryset.filter(created_at__lte=filters['end_date'])
        
        if 'search' in filters and filters['search']:
            search = filters['search']
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(message__icontains=search)
            )
        
        return [
            self.get_notification_data(notification) 
            for notification in queryset.order_by('-created_at')[:50]
        ]
    
    def get_unread_count(self):
        """
        Get the count of unread notifications.
        """
        return Notification.objects.filter(
            user=self.user,
            is_read=False
        ).count()
    
    def get_notification_data(self, notification):
        """
        Get notification data for responses.
        """
        return {
            'id': str(notification.id),
            'notification_type': notification.notification_type,
            'notification_type_display': notification.get_notification_type_display(),
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
            'created_at': notification.created_at,
        }
    
    def get_notification_templates(self, **filters):
        """
        Get a list of notification templates.
        """
        queryset = NotificationTemplate.objects.all()
        
        # Apply filters
        if 'notification_type' in filters:
            queryset = queryset.filter(notification_type=filters['notification_type'])
        
        if 'language' in filters:
            queryset = queryset.filter(language=filters['language'])
        
        if 'is_active' in filters:
            queryset = queryset.filter(is_active=filters['is_active'])
        
        return [
            self.get_notification_template_data(template) 
            for template in queryset.order_by('notification_type', 'language')
        ]
    
    def get_notification_template_data(self, template):
        """
        Get notification template data for responses.
        """
        return {
            'id': str(template.id),
            'notification_type': template.notification_type,
            'notification_type_display': template.get_notification_type_display(),
            'subject_template': template.subject_template,
            'message_template': template.message_template,
            'language': template.language,
            'language_display': template.get_language_display(),
            'is_active': template.is_active,
            'priority': template.priority,
            'priority_display': template.get_priority_display(),
            'created_at': template.created_at,
            'updated_at': template.updated_at,
        }
    
    def get_notification_preferences(self):
        """
        Get notification preferences for the current user.
        """
        try:
            preferences = NotificationPreference.objects.get(user=self.user)
            return self.get_notification_preferences_data(preferences)
        except NotificationPreference.DoesNotExist:
            return None
    
    def get_notification_preferences_data(self, preferences):
        """
        Get notification preferences data for responses.
        """
        return {
            'id': str(preferences.id),
            'user': {
                'id': str(preferences.user.id),
                'email': preferences.user.email,
                'username': preferences.user.username,
            },
            'notification_types': preferences.notification_types,
            'email_notifications': preferences.email_notifications,
            'sms_notifications': preferences.sms_notifications,
            'whatsapp_notifications': preferences.whatsapp_notifications,
            'notification_hours_start': preferences.notification_hours_start,
            'notification_hours_end': preferences.notification_hours_end,
            'play_sound': preferences.play_sound,
            'show_toast': preferences.show_toast,
            'created_at': preferences.created_at,
            'updated_at': preferences.updated_at,
        }
