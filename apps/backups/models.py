"""
Backup models.
"""
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel, UUIDModel


class Backup(UUIDModel, TimeStampedModel):
    """
    Backup model for tracking database backups.
    """
    BACKUP_TYPES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
        ('scheduled', 'Scheduled'),
    ]
    
    backup_type = models.CharField(
        _('Backup Type'),
        max_length=20,
        choices=BACKUP_TYPES,
        default='manual'
    )
    
    # User who created the backup
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='backups',
        verbose_name=_('User')
    )
    
    # File information
    file_name = models.CharField(
        _('File Name'),
        max_length=255
    )
    file_path = models.CharField(
        _('File Path'),
        max_length=500
    )
    file_size = models.PositiveBigIntegerField(
        _('File Size (bytes)'),
        default=0
    )
    
    # Organization context
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='backups',
        verbose_name=_('Organization')
    )
    
    # Backup details
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )
    
    # Status
    is_successful = models.BooleanField(
        _('Successful'),
        default=True
    )
    error_message = models.TextField(
        _('Error Message'),
        blank=True,
        null=True
    )
    
    # Verification
    is_verified = models.BooleanField(
        _('Verified'),
        default=False
    )
    verified_at = models.DateTimeField(
        _('Verified At'),
        blank=True,
        null=True
    )
    
    # Checksum
    checksum = models.CharField(
        _('Checksum'),
        max_length=128,
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('Backup')
        verbose_name_plural = _('Backups')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.file_name} ({self.get_backup_type_display()})"
    
    def get_file_size_display(self):
        """Get human-readable file size."""
        from django.utils.numberformat import format_number
        
        size_kb = self.file_size / 1024
        if size_kb < 1024:
            return f"{format_number(size_kb, 2)} KB"
        
        size_mb = size_kb / 1024
        if size_mb < 1024:
            return f"{format_number(size_mb, 2)} MB"
        
        size_gb = size_mb / 1024
        return f"{format_number(size_gb, 2)} GB"


class BackupSchedule(UUIDModel, TimeStampedModel):
    """
    Schedule for automatic backups.
    """
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    name = models.CharField(
        _('Name'),
        max_length=100
    )
    frequency = models.CharField(
        _('Frequency'),
        max_length=20,
        choices=FREQUENCY_CHOICES,
        default='daily'
    )
    
    # Schedule details
    day_of_week = models.PositiveSmallIntegerField(
        _('Day of Week'),
        choices=[
            (0, 'Monday'),
            (1, 'Tuesday'),
            (2, 'Wednesday'),
            (3, 'Thursday'),
            (4, 'Friday'),
            (5, 'Saturday'),
            (6, 'Sunday'),
        ],
        null=True,
        blank=True
    )
    day_of_month = models.PositiveSmallIntegerField(
        _('Day of Month'),
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)]
    )
    time = models.TimeField(
        _('Time'),
        default='02:00:00'
    )
    
    # Organization context
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='backup_schedules',
        verbose_name=_('Organization')
    )
    
    # Settings
    max_backups = models.PositiveIntegerField(
        _('Max Backups'),
        default=10,
        help_text=_('Maximum number of backups to keep')
    )
    backup_directory = models.CharField(
        _('Backup Directory'),
        max_length=500,
        default='backups'
    )
    
    # Status
    is_active = models.BooleanField(
        _('Active'),
        default=True
    )
    
    # Last run
    last_run = models.DateTimeField(
        _('Last Run'),
        blank=True,
        null=True
    )
    last_run_successful = models.BooleanField(
        _('Last Run Successful'),
        default=False
    )
    
    class Meta:
        verbose_name = _('Backup Schedule')
        verbose_name_plural = _('Backup Schedules')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_frequency_display()})"


class RestoreLog(UUIDModel, TimeStampedModel):
    """
    Log of backup restore operations.
    """
    backup = models.ForeignKey(
        Backup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='restore_logs',
        verbose_name=_('Backup')
    )
    
    # User who performed the restore
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='restore_logs',
        verbose_name=_('User')
    )
    
    # Restore details
    restore_path = models.CharField(
        _('Restore Path'),
        max_length=500,
        blank=True,
        null=True
    )
    
    # Status
    is_successful = models.BooleanField(
        _('Successful'),
        default=True
    )
    error_message = models.TextField(
        _('Error Message'),
        blank=True,
        null=True
    )
    
    # Timing
    started_at = models.DateTimeField(
        _('Started At'),
        blank=True,
        null=True
    )
    completed_at = models.DateTimeField(
        _('Completed At'),
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('Restore Log')
        verbose_name_plural = _('Restore Logs')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Restore from {self.backup} at {self.created_at}"
