"""
Zakat models.
"""
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from apps.core.models import TimeStampedModel, UUIDModel, ActiveModel
from decimal import Decimal


class ZakatCalculation(UUIDModel, TimeStampedModel, ActiveModel):
    """
    Model for storing zakat calculations.
    """
    # Calculation method
    CALCULATION_METHOD_CHOICES = [
        ('standard', 'Standard'),
        ('conservative', 'Conservative'),
        ('custom', 'Custom'),
    ]
    calculation_method = models.CharField(
        _('Calculation Method'),
        max_length=20,
        choices=CALCULATION_METHOD_CHOICES,
        default='standard'
    )
    
    # Organization
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='zakat_calculations',
        verbose_name=_('Organization')
    )
    
    # Calculation period
    start_date = models.DateField(
        _('Start Date')
    )
    end_date = models.DateField(
        _('End Date')
    )
    
    # Eligible assets
    eligible_cash = models.DecimalField(
        _('Eligible Cash'),
        max_digits=19,
        decimal_places=2,
        default=Decimal('0.00')
    )
    eligible_inventory = models.DecimalField(
        _('Eligible Inventory'),
        max_digits=19,
        decimal_places=2,
        default=Decimal('0.00')
    )
    eligible_receivables = models.DecimalField(
        _('Eligible Receivables'),
        max_digits=19,
        decimal_places=2,
        default=Decimal('0.00')
    )
    eligible_financial_assets = models.DecimalField(
        _('Eligible Financial Assets'),
        max_digits=19,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # Deductible liabilities
    deductible_liabilities = models.DecimalField(
        _('Deductible Liabilities'),
        max_digits=19,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # Nisab threshold
    nisab_threshold = models.DecimalField(
        _('Nisab Threshold'),
        max_digits=19,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # Calculation results
    total_eligible_assets = models.DecimalField(
        _('Total Eligible Assets'),
        max_digits=19,
        decimal_places=2,
        default=Decimal('0.00')
    )
    net_eligible_assets = models.DecimalField(
        _('Net Eligible Assets'),
        max_digits=19,
        decimal_places=2,
        default=Decimal('0.00')
    )
    zakat_amount = models.DecimalField(
        _('Zakat Amount'),
        max_digits=19,
        decimal_places=2,
        default=Decimal('0.00')
    )
    zakat_rate = models.DecimalField(
        _('Zakat Rate'),
        max_digits=5,
        decimal_places=2,
        default=Decimal('2.50')
    )
    
    # Notes
    notes = models.TextField(
        _('Notes'),
        blank=True,
        null=True
    )
    
    # User who performed the calculation
    calculated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='zakat_calculations',
        verbose_name=_('Calculated By')
    )
    
    class Meta:
        verbose_name = _('Zakat Calculation')
        verbose_name_plural = _('Zakat Calculations')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Zakat Calculation for {self.organization.name} - {self.start_date} to {self.end_date}"
    
    def calculate_zakat(self):
        """
        Calculate zakat based on the stored values.
        """
        total_eligible = (
            self.eligible_cash +
            self.eligible_inventory +
            self.eligible_receivables +
            self.eligible_financial_assets
        )
        
        net_eligible = total_eligible - self.deductible_liabilities
        
        if net_eligible >= self.nisab_threshold:
            zakat = net_eligible * (self.zakat_rate / Decimal('100'))
        else:
            zakat = Decimal('0.00')
        
        return {
            'total_eligible_assets': total_eligible,
            'net_eligible_assets': net_eligible,
            'zakat_amount': zakat,
            'nisab_threshold': self.nisab_threshold,
            'zakat_rate': self.zakat_rate,
        }


class ZakatSettings(UUIDModel, TimeStampedModel):
    """
    Settings for zakat calculations.
    """
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='zakat_settings',
        verbose_name=_('Organization')
    )
    
    # Default values
    default_nisab_threshold = models.DecimalField(
        _('Default Nisab Threshold'),
        max_digits=19,
        decimal_places=2,
        default=Decimal('0.00')
    )
    default_zakat_rate = models.DecimalField(
        _('Default Zakat Rate'),
        max_digits=5,
        decimal_places=2,
        default=Decimal('2.50')
    )
    
    # Calculation method
    default_calculation_method = models.CharField(
        _('Default Calculation Method'),
        max_length=20,
        choices=ZakatCalculation.CALCULATION_METHOD_CHOICES,
        default='standard'
    )
    
    # Eligible asset types
    include_cash = models.BooleanField(
        _('Include Cash'),
        default=True
    )
    include_inventory = models.BooleanField(
        _('Include Inventory'),
        default=True
    )
    include_receivables = models.BooleanField(
        _('Include Receivables'),
        default=True
    )
    include_financial_assets = models.BooleanField(
        _('Include Financial Assets'),
        default=True
    )
    
    # Deductible liabilities
    deduct_payables = models.BooleanField(
        _('Deduct Payables'),
        default=True
    )
    deduct_loans = models.BooleanField(
        _('Deduct Loans'),
        default=True
    )
    
    class Meta:
        verbose_name = _('Zakat Settings')
        verbose_name_plural = _('Zakat Settings')
        ordering = ['organization__name']
    
    def __str__(self):
        return f"Zakat Settings for {self.organization.name}"


class ZakatPayment(UUIDModel, TimeStampedModel):
    """
    Model for recording zakat payments.
    """
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('check', 'Check'),
        ('online', 'Online Payment'),
        ('other', 'Other'),
    ]
    
    calculation = models.ForeignKey(
        ZakatCalculation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name=_('Calculation')
    )
    
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='zakat_payments',
        verbose_name=_('Organization')
    )
    
    amount = models.DecimalField(
        _('Amount'),
        max_digits=19,
        decimal_places=2
    )
    currency = models.CharField(
        _('Currency'),
        max_length=3,
        default='DZD'
    )
    
    payment_method = models.CharField(
        _('Payment Method'),
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash'
    )
    
    payment_date = models.DateField(
        _('Payment Date'),
        default=timezone.now
    )
    
    reference = models.CharField(
        _('Reference'),
        max_length=100,
        blank=True,
        null=True
    )
    
    recipient = models.CharField(
        _('Recipient'),
        max_length=255,
        blank=True,
        null=True
    )
    
    notes = models.TextField(
        _('Notes'),
        blank=True,
        null=True
    )
    
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='zakat_payments',
        verbose_name=_('Recorded By')
    )
    
    class Meta:
        verbose_name = _('Zakat Payment')
        verbose_name_plural = _('Zakat Payments')
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"Zakat Payment - {self.amount} {self.currency} - {self.payment_date}"
