"""
Core models and abstract base models.
"""
import uuid
from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.conf import settings


class TimeStampedModel(models.Model):
    """Abstract base model with timestamps."""
    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True,
        db_index=True
    )
    updated_at = models.DateTimeField(
        _('Updated at'),
        auto_now=True,
        db_index=True
    )
    
    class Meta:
        abstract = True
        ordering = ['-created_at']


class UUIDModel(models.Model):
    """Abstract base model with UUID primary key."""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    
    @property
    def uuid(self):
        """Alias for id to maintain compatibility with existing code."""
        return self.id
    
    class Meta:
        abstract = True


class OrganizationScopedModel(models.Model):
    """Abstract base model for organization-scoped records."""
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.PROTECT,
        related_name='%(class)s_organization',
        verbose_name=_('Organization'),
        db_index=True
    )
    
    class Meta:
        abstract = True


class BranchScopedModel(models.Model):
    """Abstract base model for branch-scoped records."""
    branch = models.ForeignKey(
        'branches.Branch',
        on_delete=models.PROTECT,
        related_name='%(class)s_branch',
        verbose_name=_('Branch'),
        db_index=True
    )
    
    class Meta:
        abstract = True


class OrganizationAndBranchScopedModel(models.Model):
    """Abstract base model for organization and branch-scoped records."""
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.PROTECT,
        related_name='%(class)s_organization',
        verbose_name=_('Organization'),
        db_index=True
    )
    branch = models.ForeignKey(
        'branches.Branch',
        on_delete=models.PROTECT,
        related_name='%(class)s_branch',
        verbose_name=_('Branch'),
        db_index=True
    )
    
    class Meta:
        abstract = True


class CurrencyField(models.DecimalField):
    """Custom field for currency amounts."""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_digits', 19)
        kwargs.setdefault('decimal_places', 2)
        kwargs.setdefault('validators', [MinValueValidator(Decimal('0.00'))])
        super().__init__(*args, **kwargs)


class PercentageField(models.DecimalField):
    """Custom field for percentage values."""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_digits', 5)
        kwargs.setdefault('decimal_places', 2)
        kwargs.setdefault('validators', [
            MinValueValidator(Decimal('0.00')),
            models.MaxValueValidator(Decimal('100.00'))
        ])
        super().__init__(*args, **kwargs)


class StatusModel(models.Model):
    """Abstract base model for status tracking."""
    status = models.CharField(
        _('Status'),
        max_length=50,
        db_index=True
    )
    status_changed_at = models.DateTimeField(
        _('Status changed at'),
        auto_now=True
    )
    status_changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_status_changes',
        verbose_name=_('Changed by')
    )
    
    class Meta:
        abstract = True


class NoteModel(models.Model):
    """Abstract base model for notes."""
    notes = models.TextField(
        _('Notes'),
        blank=True,
        null=True
    )
    
    class Meta:
        abstract = True


class CodeModel(models.Model):
    """Abstract base model for code fields."""
    code = models.CharField(
        _('Code'),
        max_length=50,
        unique=True,
        db_index=True
    )
    
    class Meta:
        abstract = True


class NameModel(models.Model):
    """Abstract base model for name fields."""
    name = models.CharField(
        _('Name'),
        max_length=255
    )
    
    class Meta:
        abstract = True


class DescriptionModel(models.Model):
    """Abstract base model for description fields."""
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )
    
    class Meta:
        abstract = True


class ActiveModel(models.Model):
    """Abstract base model for active status."""
    is_active = models.BooleanField(
        _('Active'),
        default=True,
        db_index=True
    )
    
    class Meta:
        abstract = True


class AddressModel(models.Model):
    """Abstract base model for address fields."""
    address = models.TextField(
        _('Address'),
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
        _('State'),
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
    
    class Meta:
        abstract = True


class ContactModel(models.Model):
    """Abstract base model for contact information."""
    phone = models.CharField(
        _('Phone'),
        max_length=30,
        blank=True,
        null=True
    )
    secondary_phone = models.CharField(
        _('Secondary Phone'),
        max_length=30,
        blank=True,
        null=True
    )
    email = models.EmailField(
        _('Email'),
        blank=True,
        null=True
    )
    website = models.URLField(
        _('Website'),
        blank=True,
        null=True
    )
    
    class Meta:
        abstract = True


class DocumentModel(models.Model):
    """Abstract base model for document references."""
    document_number = models.CharField(
        _('Document Number'),
        max_length=50,
        blank=True,
        null=True
    )
    document_date = models.DateField(
        _('Document Date'),
        null=True,
        blank=True
    )
    
    class Meta:
        abstract = True


class FinancialModel(models.Model):
    """Abstract base model for financial fields."""
    subtotal = CurrencyField(
        _('Subtotal'),
        default=Decimal('0.00')
    )
    tax_amount = CurrencyField(
        _('Tax Amount'),
        default=Decimal('0.00')
    )
    discount_amount = CurrencyField(
        _('Discount Amount'),
        default=Decimal('0.00')
    )
    total = CurrencyField(
        _('Total'),
        default=Decimal('0.00')
    )
    
    class Meta:
        abstract = True


class BaseConfig(models.Model):
    """
    Base configuration model for storing application settings.
    """
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
    value_type = models.CharField(
        _('Value Type'),
        max_length=20,
        choices=[
            ('string', 'String'),
            ('integer', 'Integer'),
            ('float', 'Float'),
            ('boolean', 'Boolean'),
            ('json', 'JSON'),
        ],
        default='string'
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('Updated at'),
        auto_now=True
    )
    
    class Meta:
        verbose_name = _('Configuration')
        verbose_name_plural = _('Configurations')
        ordering = ['key']
    
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
        else:
            return self.value
