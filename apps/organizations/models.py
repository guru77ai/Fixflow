"""
Organization models.
"""
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from apps.core.models import TimeStampedModel, UUIDModel, AddressModel, ContactModel, ActiveModel


class Organization(UUIDModel, TimeStampedModel, AddressModel, ContactModel, ActiveModel):
    """
    Organization model representing a company or business entity.
    """
    name = models.CharField(
        _('Name'),
        max_length=255,
        validators=[MinLengthValidator(2)],
        help_text=_('The display name of the organization')
    )
    legal_name = models.CharField(
        _('Legal Name'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('The legal/registered name of the organization')
    )
    code = models.CharField(
        _('Code'),
        max_length=20,
        unique=True,
        validators=[MinLengthValidator(2)],
        help_text=_('Short code for the organization')
    )
    logo = models.ImageField(
        _('Logo'),
        upload_to='organization_logos/',
        blank=True,
        null=True
    )
    tax_identification_number = models.CharField(
        _('Tax Identification Number'),
        max_length=50,
        blank=True,
        null=True
    )
    tax_authority = models.CharField(
        _('Tax Authority'),
        max_length=100,
        blank=True,
        null=True
    )
    business_activity = models.CharField(
        _('Business Activity'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('The primary business activity of the organization')
    )
    INDUSTRY_CHOICES = [
        ('gsm_repair', 'GSM and Smartphone Repair'),
        ('computer_repair', 'Computer Repair'),
        ('electronics_repair', 'Electronics Repair'),
        ('automotive_repair', 'Automotive Repair'),
        ('general_maintenance', 'General Maintenance'),
        ('retail', 'Retail Sales'),
        ('other', 'Other'),
    ]
    
    industry = models.CharField(
        _('Industry'),
        max_length=100,
        choices=INDUSTRY_CHOICES,
        default='gsm_repair'
    )
    
    # Currency and localization
    currency = models.CharField(
        _('Currency'),
        max_length=3,
        default='DZD',
        help_text=_('ISO 4217 currency code')
    )
    LANGUAGE_CHOICES = [
        ('fr', 'Français'),
        ('ar', 'العربية'),
        ('en', 'English'),
    ]
    
    default_language = models.CharField(
        _('Default Language'),
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='fr'
    )
    timezone = models.CharField(
        _('Timezone'),
        max_length=50,
        default='Africa/Algiers'
    )
    date_format = models.CharField(
        _('Date Format'),
        max_length=20,
        default='DD/MM/YYYY'
    )
    
    # Invoice and document settings
    invoice_prefix = models.CharField(
        _('Invoice Prefix'),
        max_length=10,
        default='INV'
    )
    repair_prefix = models.CharField(
        _('Repair Prefix'),
        max_length=10,
        default='REP'
    )
    next_invoice_number = models.PositiveIntegerField(
        _('Next Invoice Number'),
        default=1
    )
    next_repair_number = models.PositiveIntegerField(
        _('Next Repair Number'),
        default=1
    )
    
    # Accounting settings
    ACCOUNTING_METHOD_CHOICES = [
        ('cash', 'Cash Basis'),
        ('accrual', 'Accrual Basis'),
    ]
    
    accounting_method = models.CharField(
        _('Accounting Method'),
        max_length=20,
        choices=ACCOUNTING_METHOD_CHOICES,
        default='accrual'
    )
    
    FISCAL_YEAR_START_CHOICES = [
        ('01', 'January'),
        ('02', 'February'),
        ('03', 'March'),
        ('04', 'April'),
        ('05', 'May'),
        ('06', 'June'),
        ('07', 'July'),
        ('08', 'August'),
        ('09', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ]
    
    fiscal_year_start = models.CharField(
        _('Fiscal Year Start'),
        max_length=2,
        choices=FISCAL_YEAR_START_CHOICES,
        default='01'
    )
    
    # License information
    license_id = models.CharField(
        _('License ID'),
        max_length=100,
        blank=True,
        null=True
    )
    license_expiry = models.DateField(
        _('License Expiry'),
        blank=True,
        null=True
    )
    
    # Notes
    notes = models.TextField(
        _('Notes'),
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('Organization')
        verbose_name_plural = _('Organizations')
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['code'],
                name='unique_organization_code'
            ),
            models.UniqueConstraint(
                fields=['tax_identification_number'],
                name='unique_organization_tax_id',
                condition=models.Q(tax_identification_number__isnull=False)
            )
        ]
    
    def __str__(self):
        return self.name
    
    def get_full_name(self):
        """Get the full name including legal name if available."""
        if self.legal_name:
            return f"{self.name} ({self.legal_name})"
        return self.name
    
    def get_logo_url(self):
        """Get the URL for the organization logo."""
        if self.logo:
            return self.logo.url
        return None
    
    def generate_next_invoice_number(self):
        """Generate the next invoice number."""
        self.next_invoice_number += 1
        self.save(update_fields=['next_invoice_number'])
        return f"{self.invoice_prefix}{self.next_invoice_number:06d}"
    
    def generate_next_repair_number(self):
        """Generate the next repair number."""
        self.next_repair_number += 1
        self.save(update_fields=['next_repair_number'])
        return f"{self.repair_prefix}{self.next_repair_number:06d}"


class OrganizationMembership(UUIDModel, TimeStampedModel):
    """
    Model representing the membership of a user in an organization.
    """
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='memberships',
        verbose_name=_('Organization')
    )
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='memberships',
        verbose_name=_('User')
    )
    role = models.ForeignKey(
        'accounts.Role',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='memberships',
        verbose_name=_('Role')
    )
    is_owner = models.BooleanField(
        _('Owner'),
        default=False,
        help_text=_('Designates whether the user is the owner of the organization')
    )
    is_admin = models.BooleanField(
        _('Administrator'),
        default=False,
        help_text=_('Designates whether the user has administrative privileges')
    )
    can_manage_users = models.BooleanField(
        _('Can Manage Users'),
        default=False
    )
    can_manage_settings = models.BooleanField(
        _('Can Manage Settings'),
        default=False
    )
    can_access_all_branches = models.BooleanField(
        _('Can Access All Branches'),
        default=False
    )
    
    class Meta:
        verbose_name = _('Organization Membership')
        verbose_name_plural = _('Organization Memberships')
        ordering = ['-is_owner', '-is_admin', 'user__email']
        constraints = [
            models.UniqueConstraint(
                fields=['organization', 'user'],
                name='unique_organization_membership'
            )
        ]
    
    def __str__(self):
        return f"{self.user} in {self.organization}"
    
    def get_permissions(self):
        """Get all permissions for this membership."""
        permissions = set()
        
        if self.is_owner or self.is_admin:
            # Owners and admins have all permissions
            return {'*': ['*']}
        
        # Get permissions from role
        if self.role:
            for perm in self.role.permissions.all():
                permissions.add(perm.codename)
        
        return permissions
