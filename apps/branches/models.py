"""
Branch models.
"""
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from apps.core.models import TimeStampedModel, UUIDModel, AddressModel, ContactModel, ActiveModel


class Branch(UUIDModel, TimeStampedModel, AddressModel, ContactModel, ActiveModel):
    """
    Branch model representing a physical location of an organization.
    """
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='branches',
        verbose_name=_('Organization')
    )
    code = models.CharField(
        _('Branch Code'),
        max_length=20,
        validators=[MinLengthValidator(2)],
        help_text=_('Short code for the branch')
    )
    name = models.CharField(
        _('Name'),
        max_length=255,
        validators=[MinLengthValidator(2)],
        help_text=_('The display name of the branch')
    )
    manager = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_branches',
        verbose_name=_('Branch Manager')
    )
    
    # Warehouse - will be added in Phase 3 when warehouses app is created
    # warehouse = models.ForeignKey(
    #     'warehouses.Warehouse',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name='branch',
    #     verbose_name=_('Warehouse')
    # )
    
    # Cash registers - will be added in Phase 4 when cash_register app is created
    # cash_registers = models.ManyToManyField(
    #     'cash_register.CashRegister',
    #     related_name='branches',
    #     verbose_name=_('Cash Registers'),
    #     blank=True
    # )
    
    # Settings
    is_main_branch = models.BooleanField(
        _('Main Branch'),
        default=False,
        help_text=_('Designates whether this is the main branch')
    )
    auto_generate_documents = models.BooleanField(
        _('Auto Generate Documents'),
        default=True,
        help_text=_('Automatically generate document numbers')
    )
    next_sale_number = models.PositiveIntegerField(
        _('Next Sale Number'),
        default=1
    )
    next_repair_number = models.PositiveIntegerField(
        _('Next Repair Number'),
        default=1
    )
    next_purchase_number = models.PositiveIntegerField(
        _('Next Purchase Number'),
        default=1
    )
    
    # Notes
    notes = models.TextField(
        _('Notes'),
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('Branch')
        verbose_name_plural = _('Branches')
        ordering = ['organization__name', 'code']
        constraints = [
            models.UniqueConstraint(
                fields=['organization', 'code'],
                name='unique_branch_code_per_organization'
            ),
            models.UniqueConstraint(
                fields=['organization', 'name'],
                name='unique_branch_name_per_organization'
            )
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def get_full_name(self):
        """Get the full name including organization."""
        return f"{self.organization.name} - {self.name}"
    
    def generate_next_sale_number(self):
        """Generate the next sale number."""
        self.next_sale_number += 1
        self.save(update_fields=['next_sale_number'])
        return self.next_sale_number
    
    def generate_next_repair_number(self):
        """Generate the next repair number."""
        self.next_repair_number += 1
        self.save(update_fields=['next_repair_number'])
        return self.next_repair_number
    
    def generate_next_purchase_number(self):
        """Generate the next purchase number."""
        self.next_purchase_number += 1
        self.save(update_fields=['next_purchase_number'])
        return self.next_purchase_number


class BranchUserAccess(UUIDModel, TimeStampedModel):
    """
    Model representing user access to specific branches.
    """
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='branch_access',
        verbose_name=_('User')
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='user_access',
        verbose_name=_('Branch')
    )
    can_access = models.BooleanField(
        _('Can Access'),
        default=True
    )
    can_manage = models.BooleanField(
        _('Can Manage'),
        default=False
    )
    
    class Meta:
        verbose_name = _('Branch User Access')
        verbose_name_plural = _('Branch User Access')
        ordering = ['user__email', 'branch__code']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'branch'],
                name='unique_branch_user_access'
            )
        ]
    
    def __str__(self):
        return f"{self.user} -> {self.branch}"
