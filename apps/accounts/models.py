"""
User model and related models for authentication.
"""
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import EmailValidator, MinLengthValidator
from apps.core.models import TimeStampedModel, UUIDModel
from .managers import UserManager


class Role(UUIDModel, TimeStampedModel):
    """
    Role model for role-based access control.
    """
    name = models.CharField(
        _('Name'),
        max_length=100,
        unique=True,
        help_text=_('Unique name for the role')
    )
    code = models.CharField(
        _('Code'),
        max_length=20,
        unique=True,
        help_text=_('Short code for the role')
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )
    is_system = models.BooleanField(
        _('System Role'),
        default=False,
        help_text=_('System roles cannot be deleted or modified')
    )
    level = models.PositiveIntegerField(
        _('Level'),
        default=0,
        help_text=_('Higher level roles have more permissions')
    )
    
    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        ordering = ['level', 'name']
    
    def __str__(self):
        return self.name
    
    def get_permissions(self):
        """Get all permissions for this role."""
        return self.permissions.all()


class Permission(UUIDModel, TimeStampedModel):
    """
    Custom permission model.
    """
    name = models.CharField(
        _('Name'),
        max_length=255,
        unique=True
    )
    codename = models.CharField(
        _('Codename'),
        max_length=100,
        unique=True,
        db_index=True
    )
    model = models.CharField(
        _('Model'),
        max_length=100,
        blank=True,
        null=True,
        help_text=_('The model this permission applies to')
    )
    action = models.CharField(
        _('Action'),
        max_length=50,
        choices=[
            ('view', 'View'),
            ('create', 'Create'),
            ('edit', 'Edit'),
            ('delete', 'Delete'),
            ('list', 'List'),
            ('validate', 'Validate'),
            ('cancel', 'Cancel'),
            ('refund', 'Refund'),
            ('export', 'Export'),
            ('print', 'Print'),
            ('access_reports', 'Access Reports'),
            ('manage_users', 'Manage Users'),
            ('manage_settings', 'Manage Settings'),
        ],
        default='view'
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('Permission')
        verbose_name_plural = _('Permissions')
        ordering = ['model', 'action', 'name']
        constraints = [
            models.UniqueConstraint(
                fields=['model', 'action'],
                name='unique_permission_action_per_model'
            )
        ]
    
    def __str__(self):
        return f"{self.name} ({self.codename})"


class User(AbstractBaseUser, PermissionsMixin, UUIDModel, TimeStampedModel):
    """
    Custom user model with organization and branch support.
    """
    email = models.EmailField(
        _('Email Address'),
        unique=True,
        validators=[EmailValidator(message=_('Enter a valid email address.'))],
        help_text=_('Required. Must be a valid email address.')
    )
    username = models.CharField(
        _('Username'),
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(3)],
        help_text=_('Required. 3-50 characters. Letters, digits and @/./+/-/_ only.')
    )
    first_name = models.CharField(
        _('First Name'),
        max_length=100,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        _('Last Name'),
        max_length=100,
        blank=True,
        null=True
    )
    phone = models.CharField(
        _('Phone'),
        max_length=30,
        blank=True,
        null=True
    )
    avatar = models.ImageField(
        _('Avatar'),
        upload_to='avatars/',
        blank=True,
        null=True
    )
    date_of_birth = models.DateField(
        _('Date of Birth'),
        blank=True,
        null=True
    )
    gender = models.CharField(
        _('Gender'),
        max_length=10,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ],
        blank=True,
        null=True
    )
    
    # Organization and branch
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.PROTECT,
        related_name='users',
        verbose_name=_('Organization'),
        null=True,
        blank=True
    )
    branch = models.ForeignKey(
        'branches.Branch',
        on_delete=models.SET_NULL,
        related_name='users',
        verbose_name=_('Branch'),
        null=True,
        blank=True
    )
    
    # Roles
    roles = models.ManyToManyField(
        Role,
        related_name='users',
        verbose_name=_('Roles'),
        blank=True
    )
    
    # Account status
    is_staff = models.BooleanField(
        _('Staff Status'),
        default=False,
        help_text=_('Designates whether the user can log into the admin site.')
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True,
        help_text=_('Designates whether this user should be treated as active.')
    )
    is_superuser = models.BooleanField(
        _('Superuser Status'),
        default=False,
        help_text=_('Designates that this user has all permissions without explicitly assigning them.')
    )
    
    # Security
    last_login = models.DateTimeField(
        _('Last Login'),
        blank=True,
        null=True
    )
    login_count = models.PositiveIntegerField(
        _('Login Count'),
        default=0
    )
    failed_login_attempts = models.PositiveIntegerField(
        _('Failed Login Attempts'),
        default=0
    )
    last_failed_login = models.DateTimeField(
        _('Last Failed Login'),
        blank=True,
        null=True
    )
    password_changed_at = models.DateTimeField(
        _('Password Changed At'),
        blank=True,
        null=True
    )
    
    # MFA
    mfa_enabled = models.BooleanField(
        _('MFA Enabled'),
        default=False
    )
    mfa_secret = models.CharField(
        _('MFA Secret'),
        max_length=255,
        blank=True,
        null=True
    )
    mfa_backup_codes = models.TextField(
        _('MFA Backup Codes'),
        blank=True,
        null=True
    )
    
    # Preferences
    language = models.CharField(
        _('Language'),
        max_length=10,
        choices=[
            ('fr', 'Français'),
            ('ar', 'العربية'),
            ('en', 'English'),
        ],
        default='fr'
    )
    timezone = models.CharField(
        _('Timezone'),
        max_length=50,
        default='Africa/Algiers'
    )
    theme = models.CharField(
        _('Theme'),
        max_length=20,
        choices=[
            ('light', 'Light'),
            ('dark', 'Dark'),
            ('system', 'System'),
        ],
        default='system'
    )
    
    # Tracking
    created_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_users'
    )
    updated_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_users'
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['email'],
                name='unique_user_email'
            ),
            models.UniqueConstraint(
                fields=['username'],
                name='unique_user_username'
            )
        ]
    
    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name} ({self.email})"
        return f"{self.username} ({self.email})"
    
    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()
    
    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name or self.username
    
    def get_roles(self):
        """Get all roles for the user."""
        return self.roles.all()
    
    def has_role(self, role_name):
        """Check if user has a specific role."""
        return self.roles.filter(name=role_name).exists()
    
    def get_permissions(self):
        """Get all permissions for the user."""
        permissions = set()
        
        # Get permissions from roles
        for role in self.roles.all():
            for perm in role.permissions.all():
                permissions.add(perm.codename)
        
        # Add Django model permissions
        if self.is_superuser:
            permissions.update(self.get_all_permissions())
        
        return permissions
    
    def has_perm(self, perm, obj=None):
        """Check if user has a specific permission."""
        if self.is_superuser:
            return True
        
        # Check role permissions
        if perm in self.get_permissions():
            return True
        
        # Check Django model permissions
        return super().has_perm(perm, obj)
    
    def has_module_perms(self, app_label):
        """Check if user has any permissions for a module."""
        if self.is_superuser:
            return True
        
        # Check if user has any permission for this module
        for role in self.roles.all():
            if role.permissions.filter(model__icontains=app_label).exists():
                return True
        
        return super().has_module_perms(app_label)
    
    def get_avatar_url(self):
        """Get the URL for the user's avatar."""
        if self.avatar:
            return self.avatar.url
        return None
    
    def increment_login_count(self):
        """Increment the login count."""
        self.login_count += 1
        self.last_login = timezone.now()
        self.save(update_fields=['login_count', 'last_login'])
    
    def increment_failed_login(self):
        """Increment the failed login count."""
        self.failed_login_attempts += 1
        self.last_failed_login = timezone.now()
        self.save(update_fields=['failed_login_attempts', 'last_failed_login'])
    
    def reset_failed_login(self):
        """Reset the failed login count."""
        self.failed_login_attempts = 0
        self.save(update_fields=['failed_login_attempts'])
    
    def is_locked(self):
        """Check if the user account is locked due to too many failed attempts."""
        return self.failed_login_attempts >= 5


class UserSession(UUIDModel, TimeStampedModel):
    """
    Track user login sessions.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sessions',
        verbose_name=_('User')
    )
    session_key = models.CharField(
        _('Session Key'),
        max_length=40,
        unique=True,
        db_index=True
    )
    ip_address = models.GenericIPAddressField(
        _('IP Address'),
        blank=True,
        null=True
    )
    user_agent = models.TextField(
        _('User Agent'),
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True
    )
    expired_at = models.DateTimeField(
        _('Expired At'),
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('User Session')
        verbose_name_plural = _('User Sessions')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user} - {self.session_key}"


class LoginHistory(UUIDModel, TimeStampedModel):
    """
    Track user login history.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='login_history',
        verbose_name=_('User')
    )
    ip_address = models.GenericIPAddressField(
        _('IP Address'),
        blank=True,
        null=True
    )
    user_agent = models.TextField(
        _('User Agent'),
        blank=True,
        null=True
    )
    login_time = models.DateTimeField(
        _('Login Time'),
        auto_now_add=True
    )
    logout_time = models.DateTimeField(
        _('Logout Time'),
        blank=True,
        null=True
    )
    is_successful = models.BooleanField(
        _('Successful'),
        default=True
    )
    failure_reason = models.CharField(
        _('Failure Reason'),
        max_length=255,
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('Login History')
        verbose_name_plural = _('Login History')
        ordering = ['-login_time']
    
    def __str__(self):
        return f"{self.user} - {self.login_time}"


class PasswordResetToken(UUIDModel, TimeStampedModel):
    """
    Track password reset tokens.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='password_reset_tokens',
        verbose_name=_('User')
    )
    token = models.CharField(
        _('Token'),
        max_length=255,
        unique=True,
        db_index=True
    )
    expires_at = models.DateTimeField(
        _('Expires At')
    )
    is_used = models.BooleanField(
        _('Used'),
        default=False
    )
    
    class Meta:
        verbose_name = _('Password Reset Token')
        verbose_name_plural = _('Password Reset Tokens')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user} - {self.token[:20]}..."
    
    def is_valid(self):
        """Check if the token is still valid."""
        return not self.is_used and self.expires_at > timezone.now()


class UserPreference(UUIDModel, TimeStampedModel):
    """
    Store user preferences.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='preferences',
        verbose_name=_('User')
    )
    dashboard_layout = models.JSONField(
        _('Dashboard Layout'),
        default=dict,
        blank=True
    )
    notifications_enabled = models.BooleanField(
        _('Notifications Enabled'),
        default=True
    )
    email_notifications = models.BooleanField(
        _('Email Notifications'),
        default=True
    )
    sms_notifications = models.BooleanField(
        _('SMS Notifications'),
        default=False
    )
    
    class Meta:
        verbose_name = _('User Preference')
        verbose_name_plural = _('User Preferences')
    
    def __str__(self):
        return f"Preferences for {self.user}"
