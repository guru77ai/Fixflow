"""
License models for perpetual license verification.
"""
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from apps.core.models import TimeStampedModel, UUIDModel, ActiveModel


class License(UUIDModel, TimeStampedModel, ActiveModel):
    """
    License model for storing license information.
    """
    # License identification
    license_id = models.CharField(
        _('License ID'),
        max_length=100,
        unique=True,
        validators=[MinLengthValidator(10)],
        db_index=True
    )
    
    # Customer information
    customer_name = models.CharField(
        _('Customer Name'),
        max_length=255
    )
    customer_email = models.EmailField(
        _('Customer Email'),
        blank=True,
        null=True
    )
    customer_phone = models.CharField(
        _('Customer Phone'),
        max_length=30,
        blank=True,
        null=True
    )
    
    # Product edition
    EDITION_CHOICES = [
        ('starter', 'Starter'),
        ('professional', 'Professional'),
        ('enterprise', 'Enterprise'),
        ('custom', 'Custom'),
    ]
    edition = models.CharField(
        _('Edition'),
        max_length=20,
        choices=EDITION_CHOICES,
        default='professional'
    )
    
    # Enabled modules
    enabled_modules = models.JSONField(
        _('Enabled Modules'),
        default=list,
        blank=True,
        help_text=_('List of enabled module codes')
    )
    
    # License dates
    issue_date = models.DateField(
        _('Issue Date')
    )
    expiry_date = models.DateField(
        _('Expiry Date'),
        null=True,
        blank=True,
        help_text=_('Leave blank for perpetual license')
    )
    
    # Installation binding
    INSTALLATION_BINDING_CHOICES = [
        ('none', 'No Binding'),
        ('machine_id', 'Machine ID'),
        ('mac_address', 'MAC Address'),
        ('hardware_id', 'Hardware ID'),
    ]
    installation_binding = models.CharField(
        _('Installation Binding'),
        max_length=20,
        choices=INSTALLATION_BINDING_CHOICES,
        default='none'
    )
    bound_to = models.CharField(
        _('Bound To'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('The value the license is bound to')
    )
    max_installations = models.PositiveIntegerField(
        _('Max Installations'),
        default=1,
        help_text=_('Maximum number of installations allowed')
    )
    
    # License status
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('suspended', 'Suspended'),
        ('revoked', 'Revoked'),
        ('invalid', 'Invalid'),
    ]
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    status_reason = models.TextField(
        _('Status Reason'),
        blank=True,
        null=True
    )
    
    # Signature data (stored for verification)
    signature = models.TextField(
        _('Signature'),
        blank=True,
        null=True,
        help_text=_('Digital signature of the license data')
    )
    signed_data = models.TextField(
        _('Signed Data'),
        blank=True,
        null=True,
        help_text=_('The data that was signed')
    )
    
    # Verification
    last_verified = models.DateTimeField(
        _('Last Verified'),
        blank=True,
        null=True
    )
    verification_count = models.PositiveIntegerField(
        _('Verification Count'),
        default=0
    )
    
    # Maintenance and upgrades
    maintenance_expires = models.DateField(
        _('Maintenance Expires'),
        null=True,
        blank=True,
        help_text=_('Date when maintenance/support expires')
    )
    can_upgrade = models.BooleanField(
        _('Can Upgrade'),
        default=True
    )
    
    # Notes
    notes = models.TextField(
        _('Notes'),
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('License')
        verbose_name_plural = _('Licenses')
        ordering = ['-issue_date', 'customer_name']
        constraints = [
            models.UniqueConstraint(
                fields=['license_id'],
                name='unique_license_id'
            )
        ]
    
    def __str__(self):
        return f"{self.license_id} - {self.customer_name}"
    
    def is_perpetual(self):
        """Check if the license is perpetual."""
        return self.expiry_date is None
    
    def is_expired(self):
        """Check if the license has expired."""
        from django.utils import timezone
        if self.expiry_date is None:
            return False
        return self.expiry_date < timezone.now().date()
    
    def is_valid(self):
        """Check if the license is valid."""
        return (
            self.is_active and
            not self.is_expired() and
            self.status == 'active'
        )
    
    def has_module(self, module_code):
        """Check if a module is enabled."""
        return module_code in self.enabled_modules
    
    def get_module_display_name(self, module_code):
        """Get the display name for a module."""
        module_names = {
            'core': 'Core',
            'accounts': 'Accounts',
            'organizations': 'Organizations',
            'licensing': 'Licensing',
            'branches': 'Branches',
            'dashboard': 'Dashboard',
            'customers': 'Customers',
            'suppliers': 'Suppliers',
            'devices': 'Devices',
            'repairs': 'Repairs',
            'technicians': 'Technicians',
            'products': 'Products',
            'categories': 'Categories',
            'inventory': 'Inventory',
            'warehouses': 'Warehouses',
            'stock_transfers': 'Stock Transfers',
            'purchasing': 'Purchasing',
            'sales': 'Sales',
            'pos': 'Point of Sale',
            'invoicing': 'Invoicing',
            'payments': 'Payments',
            'installments': 'Installments',
            'cash_register': 'Cash Register',
            'expenses': 'Expenses',
            'accounting': 'Accounting',
            'employees': 'Employees',
            'attendance': 'Attendance',
            'payroll': 'Payroll',
            'commissions': 'Commissions',
            'notifications': 'Notifications',
            'reports': 'Reports',
            'documents': 'Documents',
            'barcode': 'Barcode',
            'audit_logs': 'Audit Logs',
            'backups': 'Backups',
            'settings': 'Settings',
            'zakat': 'Zakat',
        }
        return module_names.get(module_code, module_code)


class LicenseVerificationLog(UUIDModel, TimeStampedModel):
    """
    Log of license verification attempts.
    """
    license = models.ForeignKey(
        License,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verification_logs',
        verbose_name=_('License')
    )
    license_identifier = models.CharField(
        _('License ID'),
        max_length=100,
        db_index=True
    )
    is_valid = models.BooleanField(
        _('Valid'),
        default=False
    )
    error_message = models.TextField(
        _('Error Message'),
        blank=True,
        null=True
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
    
    class Meta:
        verbose_name = _('License Verification Log')
        verbose_name_plural = _('License Verification Logs')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.license_identifier} - {'Valid' if self.is_valid else 'Invalid'}"


class Installation(UUIDModel, TimeStampedModel):
    """
    Model representing an installation of the software.
    """
    license = models.ForeignKey(
        License,
        on_delete=models.CASCADE,
        related_name='installations',
        verbose_name=_('License')
    )
    installation_id = models.CharField(
        _('Installation ID'),
        max_length=100,
        unique=True,
        db_index=True
    )
    machine_name = models.CharField(
        _('Machine Name'),
        max_length=255,
        blank=True,
        null=True
    )
    machine_id = models.CharField(
        _('Machine ID'),
        max_length=255,
        blank=True,
        null=True
    )
    mac_address = models.CharField(
        _('MAC Address'),
        max_length=255,
        blank=True,
        null=True
    )
    hardware_id = models.CharField(
        _('Hardware ID'),
        max_length=255,
        blank=True,
        null=True
    )
    ip_address = models.GenericIPAddressField(
        _('IP Address'),
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True
    )
    last_active = models.DateTimeField(
        _('Last Active'),
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('Installation')
        verbose_name_plural = _('Installations')
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['license', 'installation_id'],
                name='unique_installation_per_license'
            )
        ]
    
    def __str__(self):
        return f"{self.installation_id} - {self.machine_name}"
