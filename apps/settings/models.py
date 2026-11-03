"""
Application settings models.
"""
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.core.models import TimeStampedModel, UUIDModel


class SettingCategory(UUIDModel, TimeStampedModel):
    """
    Category for organizing settings.
    """
    name = models.CharField(
        _('Name'),
        max_length=100,
        unique=True
    )
    code = models.CharField(
        _('Code'),
        max_length=50,
        unique=True
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )
    order = models.PositiveIntegerField(
        _('Order'),
        default=0
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True
    )
    
    class Meta:
        verbose_name = _('Setting Category')
        verbose_name_plural = _('Setting Categories')
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class SystemSetting(UUIDModel, TimeStampedModel):
    """
    System-wide settings.
    """
    category = models.ForeignKey(
        SettingCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='system_settings',
        verbose_name=_('Category')
    )
    
    key = models.CharField(
        _('Key'),
        max_length=100,
        unique=True,
        db_index=True
    )
    value = models.TextField(
        _('Value'),
        blank=True,
        null=True
    )
    
    VALUE_TYPE_CHOICES = [
        ('string', 'String'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('boolean', 'Boolean'),
        ('json', 'JSON'),
        ('date', 'Date'),
        ('datetime', 'DateTime'),
    ]
    value_type = models.CharField(
        _('Value Type'),
        max_length=20,
        choices=VALUE_TYPE_CHOICES,
        default='string'
    )
    
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )
    
    is_editable = models.BooleanField(
        _('Editable'),
        default=True
    )
    
    is_public = models.BooleanField(
        _('Public'),
        default=False,
        help_text=_('Public settings can be accessed without authentication')
    )
    
    class Meta:
        verbose_name = _('System Setting')
        verbose_name_plural = _('System Settings')
        ordering = ['category__order', 'key']
    
    def __str__(self):
        return f"{self.key} = {self.value}"
    
    def get_value(self):
        """Get the value in the correct type."""
        if self.value is None:
            return None
        
        if self.value_type == 'integer':
            return int(self.value)
        elif self.value_type == 'float':
            return float(self.value)
        elif self.value_type == 'boolean':
            return self.value.lower() in ('true', '1', 'yes', 'on')
        elif self.value_type == 'json':
            import json
            return json.loads(self.value)
        elif self.value_type == 'date':
            from django.utils.dateparse import parse_date
            return parse_date(self.value)
        elif self.value_type == 'datetime':
            from django.utils.dateparse import parse_datetime
            return parse_datetime(self.value)
        else:
            return self.value


class OrganizationSetting(UUIDModel, TimeStampedModel):
    """
    Organization-specific settings.
    """
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='settings',
        verbose_name=_('Organization')
    )
    
    category = models.ForeignKey(
        SettingCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='organization_settings',
        verbose_name=_('Category')
    )
    
    key = models.CharField(
        _('Key'),
        max_length=100,
        db_index=True
    )
    value = models.TextField(
        _('Value'),
        blank=True,
        null=True
    )
    
    VALUE_TYPE_CHOICES = [
        ('string', 'String'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('boolean', 'Boolean'),
        ('json', 'JSON'),
        ('date', 'Date'),
        ('datetime', 'DateTime'),
    ]
    value_type = models.CharField(
        _('Value Type'),
        max_length=20,
        choices=VALUE_TYPE_CHOICES,
        default='string'
    )
    
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('Organization Setting')
        verbose_name_plural = _('Organization Settings')
        ordering = ['organization', 'category__order', 'key']
        constraints = [
            models.UniqueConstraint(
                fields=['organization', 'key'],
                name='unique_organization_setting_key'
            )
        ]
    
    def __str__(self):
        return f"{self.organization} - {self.key} = {self.value}"
    
    def get_value(self):
        """Get the value in the correct type."""
        if self.value is None:
            return None
        
        if self.value_type == 'integer':
            return int(self.value)
        elif self.value_type == 'float':
            return float(self.value)
        elif self.value_type == 'boolean':
            return self.value.lower() in ('true', '1', 'yes', 'on')
        elif self.value_type == 'json':
            import json
            return json.loads(self.value)
        elif self.value_type == 'date':
            from django.utils.dateparse import parse_date
            return parse_date(self.value)
        elif self.value_type == 'datetime':
            from django.utils.dateparse import parse_datetime
            return parse_datetime(self.value)
        else:
            return self.value


class BranchSetting(UUIDModel, TimeStampedModel):
    """
    Branch-specific settings.
    """
    branch = models.ForeignKey(
        'branches.Branch',
        on_delete=models.CASCADE,
        related_name='settings',
        verbose_name=_('Branch')
    )
    
    category = models.ForeignKey(
        SettingCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='branch_settings',
        verbose_name=_('Category')
    )
    
    key = models.CharField(
        _('Key'),
        max_length=100,
        db_index=True
    )
    value = models.TextField(
        _('Value'),
        blank=True,
        null=True
    )
    
    VALUE_TYPE_CHOICES = [
        ('string', 'String'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('boolean', 'Boolean'),
        ('json', 'JSON'),
        ('date', 'Date'),
        ('datetime', 'DateTime'),
    ]
    value_type = models.CharField(
        _('Value Type'),
        max_length=20,
        choices=VALUE_TYPE_CHOICES,
        default='string'
    )
    
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('Branch Setting')
        verbose_name_plural = _('Branch Settings')
        ordering = ['branch__organization', 'branch__code', 'category__order', 'key']
        constraints = [
            models.UniqueConstraint(
                fields=['branch', 'key'],
                name='unique_branch_setting_key'
            )
        ]
    
    def __str__(self):
        return f"{self.branch} - {self.key} = {self.value}"
    
    def get_value(self):
        """Get the value in the correct type."""
        if self.value is None:
            return None
        
        if self.value_type == 'integer':
            return int(self.value)
        elif self.value_type == 'float':
            return float(self.value)
        elif self.value_type == 'boolean':
            return self.value.lower() in ('true', '1', 'yes', 'on')
        elif self.value_type == 'json':
            import json
            return json.loads(self.value)
        elif self.value_type == 'date':
            from django.utils.dateparse import parse_date
            return parse_date(self.value)
        elif self.value_type == 'datetime':
            from django.utils.dateparse import parse_datetime
            return parse_datetime(self.value)
        else:
            return self.value


class UserSetting(UUIDModel, TimeStampedModel):
    """
    User-specific settings.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_settings',
        verbose_name=_('User')
    )
    
    key = models.CharField(
        _('Key'),
        max_length=100,
        db_index=True
    )
    value = models.TextField(
        _('Value'),
        blank=True,
        null=True
    )
    
    VALUE_TYPE_CHOICES = [
        ('string', 'String'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('boolean', 'Boolean'),
        ('json', 'JSON'),
        ('date', 'Date'),
        ('datetime', 'DateTime'),
    ]
    value_type = models.CharField(
        _('Value Type'),
        max_length=20,
        choices=VALUE_TYPE_CHOICES,
        default='string'
    )
    
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('User Setting')
        verbose_name_plural = _('User Settings')
        ordering = ['user__email', 'key']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'key'],
                name='unique_user_setting_key'
            )
        ]
    
    def __str__(self):
        return f"{self.user} - {self.key} = {self.value}"
    
    def get_value(self):
        """Get the value in the correct type."""
        if self.value is None:
            return None
        
        if self.value_type == 'integer':
            return int(self.value)
        elif self.value_type == 'float':
            return float(self.value)
        elif self.value_type == 'boolean':
            return self.value.lower() in ('true', '1', 'yes', 'on')
        elif self.value_type == 'json':
            import json
            return json.loads(self.value)
        elif self.value_type == 'date':
            from django.utils.dateparse import parse_date
            return parse_date(self.value)
        elif self.value_type == 'datetime':
            from django.utils.dateparse import parse_datetime
            return parse_datetime(self.value)
        else:
            return self.value
