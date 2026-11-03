"""
Notification models.
"""
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.core.models import TimeStampedModel, UUIDModel


class NotificationType(UUIDModel, TimeStampedModel):
    """
    Notification type model.
    """
    code = models.CharField(
        _('Code'),
        max_length=50,
        unique=True,
        db_index=True
    )
    name = models.CharField(
        _('Name'),
        max_length=100,
        unique=True
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True
    )
    
    class Meta:
        verbose_name = _('Notification Type')
        verbose_name_plural = _('Notification Types')
        ordering = ['code']
    
    def __str__(self):
        return self.name


class Notification(UUIDModel, TimeStampedModel):
    """
    Notification model.
    """
    NOTIFICATION_TYPES = [
        ('repair_received', 'Repair Received'),
        ('diagnosis_completed', 'Diagnosis Completed'),
        ('quotation_awaiting_approval', 'Quotation Awaiting Approval'),
        ('parts_unavailable', 'Parts Unavailable'),
        ('repair_ready', 'Repair Ready'),
        ('repair_delivered', 'Repair Delivered'),
        ('payment_received', 'Payment Received'),
        ('installment_overdue', 'Installment Overdue'),
        ('low_stock', 'Low Stock'),
        ('purchase_received', 'Purchase Received'),
        ('warranty_reminder', 'Warranty Reminder'),
        ('cash_register_alert', 'Cash Register Alert'),
        ('expense_approval', 'Expense Approval'),
        ('payroll_processed', 'Payroll Processed'),
        ('system_alert', 'System Alert'),
    ]
    
    notification_type = models.CharField(
        _('Type'),
        max_length=50,
        choices=NOTIFICATION_TYPES,
        db_index=True
    )
    
    # Recipient
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_('User')
    )
    
    # Content
    title = models.CharField(
        _('Title'),
        max_length=255
    )
    message = models.TextField(
        _('Message')
    )
    
    # Related entity
    entity_type = models.CharField(
        _('Entity Type'),
        max_length=100,
        blank=True,
        null=True
    )
    entity_id = models.UUIDField(
        _('Entity ID'),
        null=True,
        blank=True
    )
    entity_url = models.URLField(
        _('Entity URL'),
        max_length=500,
        blank=True,
        null=True
    )
    
    # Organization and branch context
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications',
        verbose_name=_('Organization')
    )
    branch = models.ForeignKey(
        'branches.Branch',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications',
        verbose_name=_('Branch')
    )
    
    # Status
    is_read = models.BooleanField(
        _('Read'),
        default=False
    )
    is_archived = models.BooleanField(
        _('Archived'),
        default=False
    )
    
    # Priority
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    priority = models.CharField(
        _('Priority'),
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    
    # Delivery
    is_delivered = models.BooleanField(
        _('Delivered'),
        default=False
    )
    delivered_at = models.DateTimeField(
        _('Delivered At'),
        blank=True,
        null=True
    )
    delivery_method = models.CharField(
        _('Delivery Method'),
        max_length=20,
        choices=[
            ('in_app', 'In-App'),
            ('email', 'Email'),
            ('sms', 'SMS'),
            ('whatsapp', 'WhatsApp'),
        ],
        default='in_app'
    )
    
    # Actions
    actions = models.JSONField(
        _('Actions'),
        default=list,
        blank=True,
        help_text=_('List of available actions for this notification')
    )
    
    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['notification_type', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user}"
    
    def mark_as_read(self):
        """Mark the notification as read."""
        self.is_read = True
        self.save(update_fields=['is_read'])
    
    def mark_as_archived(self):
        """Mark the notification as archived."""
        self.is_archived = True
        self.save(update_fields=['is_archived'])
    
    @classmethod
    def create_notification(cls, user, notification_type, title, message, **kwargs):
        """
        Helper method to create a notification.
        """
        notification = cls(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            entity_type=kwargs.get('entity_type'),
            entity_id=kwargs.get('entity_id'),
            entity_url=kwargs.get('entity_url'),
            organization=kwargs.get('organization'),
            branch=kwargs.get('branch'),
            priority=kwargs.get('priority', 'medium'),
            delivery_method=kwargs.get('delivery_method', 'in_app'),
            actions=kwargs.get('actions', []),
        )
        notification.save()
        return notification


class NotificationTemplate(UUIDModel, TimeStampedModel):
    """
    Template for notifications.
    """
    notification_type = models.CharField(
        _('Notification Type'),
        max_length=50,
        choices=Notification.NOTIFICATION_TYPES,
        unique=True,
        db_index=True
    )
    
    # Template content
    subject_template = models.CharField(
        _('Subject Template'),
        max_length=255
    )
    message_template = models.TextField(
        _('Message Template')
    )
    
    # Language
    LANGUAGE_CHOICES = [
        ('fr', 'Français'),
        ('ar', 'العربية'),
        ('en', 'English'),
    ]
    language = models.CharField(
        _('Language'),
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='fr'
    )
    
    # Delivery settings
    is_active = models.BooleanField(
        _('Active'),
        default=True
    )
    priority = models.CharField(
        _('Priority'),
        max_length=10,
        choices=Notification.PRIORITY_CHOICES,
        default='medium'
    )
    
    class Meta:
        verbose_name = _('Notification Template')
        verbose_name_plural = _('Notification Templates')
        ordering = ['notification_type', 'language']
        constraints = [
            models.UniqueConstraint(
                fields=['notification_type', 'language'],
                name='unique_notification_template'
            )
        ]
    
    def __str__(self):
        return f"{self.notification_type} ({self.language})"
    
    def render(self, context):
        """
        Render the template with the given context.
        """
        from django.template import Template, Context
        
        template = Template(self.message_template)
        context = Context(context)
        return template.render(context)


class NotificationPreference(UUIDModel, TimeStampedModel):
    """
    User notification preferences.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notification_preferences',
        verbose_name=_('User')
    )
    
    # Notification type preferences
    notification_types = models.JSONField(
        _('Notification Types'),
        default=dict,
        blank=True,
        help_text=_('Dictionary of notification type preferences')
    )
    
    # Delivery preferences
    email_notifications = models.BooleanField(
        _('Email Notifications'),
        default=True
    )
    sms_notifications = models.BooleanField(
        _('SMS Notifications'),
        default=False
    )
    whatsapp_notifications = models.BooleanField(
        _('WhatsApp Notifications'),
        default=False
    )
    
    # Timing preferences
    notification_hours_start = models.TimeField(
        _('Notification Hours Start'),
        default='08:00:00'
    )
    notification_hours_end = models.TimeField(
        _('Notification Hours End'),
        default='20:00:00'
    )
    
    # Sound and display
    play_sound = models.BooleanField(
        _('Play Sound'),
        default=True
    )
    show_toast = models.BooleanField(
        _('Show Toast'),
        default=True
    )
    
    class Meta:
        verbose_name = _('Notification Preference')
        verbose_name_plural = _('Notification Preferences')
    
    def __str__(self):
        return f"Preferences for {self.user}"
    
    def is_notification_enabled(self, notification_type):
        """Check if a notification type is enabled."""
        preferences = self.notification_types.get(notification_type, {})
        return preferences.get('enabled', True)
