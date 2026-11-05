"""
Supplier Models for FixSoftRepair Pro
Supplier Management module
"""
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from apps.core.models import TimeStampedModel, UUIDModel, OrganizationAndBranchScopedModel, NoteModel


class SupplierCategory(UUIDModel, TimeStampedModel):
    """
    Supplier category (e.g., Parts Supplier, Service Provider, etc.)
    """
    name = models.CharField(
        _('Name'),
        max_length=100,
        unique=True
    )
    code = models.CharField(
        _('Code'),
        max_length=10,
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
        verbose_name = _('Supplier Category')
        verbose_name_plural = _('Supplier Categories')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Supplier(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel, NoteModel):
    """
    Supplier model
    """
    SUPPLIER_STATUS_CHOICES = [
        ('active', _('Active')),
        ('inactive', _('Inactive')),
        ('blocked', _('Blocked')),
        ('prospect', _('Prospect')),
    ]
    
    category = models.ForeignKey(
        SupplierCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='suppliers',
        verbose_name=_('Category')
    )
    
    # Basic information
    code = models.CharField(
        _('Code'),
        max_length=20,
        unique=True,
        db_index=True
    )
    name = models.CharField(
        _('Name'),
        max_length=200
    )
    company_name = models.CharField(
        _('Company Name'),
        max_length=200,
        blank=True,
        null=True
    )
    
    # Contact information
    email = models.EmailField(
        _('Email'),
        blank=True,
        null=True
    )
    phone = PhoneNumberField(
        _('Phone'),
        blank=True,
        null=True
    )
    mobile = PhoneNumberField(
        _('Mobile'),
        blank=True,
        null=True
    )
    website = models.URLField(
        _('Website'),
        blank=True,
        null=True
    )
    
    # Address
    address_line_1 = models.CharField(
        _('Address Line 1'),
        max_length=255,
        blank=True,
        null=True
    )
    address_line_2 = models.CharField(
        _('Address Line 2'),
        max_length=255,
        blank=True,
        null=True
    )
    city = models.CharField(
        _('City'),
        max_length=100,
        blank=True,
        null=True
    )
    state = models.CharField(
        _('State/Province'),
        max_length=100,
        blank=True,
        null=True
    )
    postal_code = models.CharField(
        _('Postal Code'),
        max_length=20,
        blank=True,
        null=True
    )
    country = models.CharField(
        _('Country'),
        max_length=100,
        default='Algeria'
    )
    
    # Tax information
    tax_id = models.CharField(
        _('Tax ID'),
        max_length=50,
        blank=True,
        null=True
    )
    
    # Financial information
    payment_terms = models.CharField(
        _('Payment Terms'),
        max_length=100,
        blank=True,
        null=True
    )
    credit_limit = models.DecimalField(
        _('Credit Limit'),
        max_digits=19,
        decimal_places=2,
        default=0.00
    )
    credit_balance = models.DecimalField(
        _('Credit Balance'),
        max_digits=19,
        decimal_places=2,
        default=0.00
    )
    
    # Status
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=SUPPLIER_STATUS_CHOICES,
        default='active'
    )
    
    # Ratings
    quality_rating = models.PositiveIntegerField(
        _('Quality Rating'),
        default=5,
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )
    delivery_rating = models.PositiveIntegerField(
        _('Delivery Rating'),
        default=5,
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )
    
    # Account manager
    account_manager = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_suppliers',
        verbose_name=_('Account Manager')
    )
    
    # Metadata
    is_verified = models.BooleanField(
        _('Verified'),
        default=False
    )
    is_preferred = models.BooleanField(
        _('Preferred Supplier'),
        default=False
    )
    
    class Meta:
        verbose_name = _('Supplier')
        verbose_name_plural = _('Suppliers')
        ordering = ['name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['name']),
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    @property
    def display_name(self):
        """Display name with code."""
        return f"{self.code} - {self.name}"
    
    @property
    def full_name(self):
        """Get full name."""
        if self.company_name:
            return self.company_name
        return self.name
    
    @property
    def address(self):
        """Get formatted address."""
        parts = [
            self.address_line_1,
            self.address_line_2,
            self.city,
            self.state,
            self.postal_code,
            self.country
        ]
        return ', '.join(filter(None, parts))


class SupplierContact(UUIDModel, TimeStampedModel):
    """
    Contact person for a supplier
    """
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name='contacts',
        verbose_name=_('Supplier')
    )
    first_name = models.CharField(
        _('First Name'),
        max_length=100
    )
    last_name = models.CharField(
        _('Last Name'),
        max_length=100,
        blank=True,
        null=True
    )
    position = models.CharField(
        _('Position'),
        max_length=100,
        blank=True,
        null=True
    )
    email = models.EmailField(
        _('Email'),
        blank=True,
        null=True
    )
    phone = PhoneNumberField(
        _('Phone'),
        blank=True,
        null=True
    )
    mobile = PhoneNumberField(
        _('Mobile'),
        blank=True,
        null=True
    )
    is_primary = models.BooleanField(
        _('Primary Contact'),
        default=False
    )
    notes = models.TextField(
        _('Notes'),
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('Supplier Contact')
        verbose_name_plural = _('Supplier Contacts')
        ordering = ['first_name', 'last_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name or ''} - {self.supplier.name}".strip()


class SupplierDocument(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """
    Documents for suppliers (contracts, certificates, etc.)
    """
    DOCUMENT_TYPE_CHOICES = [
        ('contract', _('Contract')),
        ('certificate', _('Certificate')),
        ('catalog', _('Product Catalog')),
        ('price_list', _('Price List')),
        ('tax_certificate', _('Tax Certificate')),
        ('business_license', _('Business License')),
        ('other', _('Other')),
    ]
    
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name=_('Supplier')
    )
    document_type = models.CharField(
        _('Type'),
        max_length=30,
        choices=DOCUMENT_TYPE_CHOICES
    )
    title = models.CharField(
        _('Title'),
        max_length=200
    )
    file = models.FileField(
        _('File'),
        upload_to='supplier_documents/'
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )
    expiry_date = models.DateField(
        _('Expiry Date'),
        blank=True,
        null=True
    )
    is_verified = models.BooleanField(
        _('Verified'),
        default=False
    )
    
    class Meta:
        verbose_name = _('Supplier Document')
        verbose_name_plural = _('Supplier Documents')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.supplier.name} - {self.title}"
