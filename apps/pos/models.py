"""
POS Models for FixSoftRepair Pro
Point of Sale module
"""
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel, UUIDModel, OrganizationAndBranchScopedModel, NoteModel, CurrencyField


class PaymentMethod(UUIDModel, TimeStampedModel):
    """Payment methods (Cash, Card, Mobile, etc.)"""
    name = models.CharField(_('Name'), max_length=50, unique=True)
    code = models.CharField(_('Code'), max_length=10, unique=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    is_active = models.BooleanField(_('Active'), default=True)
    is_cash = models.BooleanField(_('Cash'), default=False)
    is_card = models.BooleanField(_('Card'), default=False)
    is_mobile = models.BooleanField(_('Mobile'), default=False)
    is_online = models.BooleanField(_('Online'), default=False)
    icon = models.CharField(_('Icon'), max_length=50, blank=True, null=True)
    
    class Meta:
        verbose_name = _('Payment Method')
        verbose_name_plural = _('Payment Methods')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class CashRegister(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """Cash register/terminal for POS"""
    name = models.CharField(_('Name'), max_length=100)
    code = models.CharField(_('Code'), max_length=20, unique=True)
    initial_amount = CurrencyField(_('Initial Amount'), default=0.00)
    current_amount = CurrencyField(_('Current Amount'), default=0.00)
    is_active = models.BooleanField(_('Active'), default=True)
    is_open = models.BooleanField(_('Open'), default=False)
    opened_at = models.DateTimeField(_('Opened At'), blank=True, null=True)
    closed_at = models.DateTimeField(_('Closed At'), blank=True, null=True)
    opened_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='opened_registers', verbose_name=_('Opened By'))
    closed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='closed_registers', verbose_name=_('Closed By'))
    
    class Meta:
        verbose_name = _('Cash Register')
        verbose_name_plural = _('Cash Registers')
        ordering = ['name']
        unique_together = [['organization', 'code']]
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class Sale(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel, NoteModel):
    """Sale transaction"""
    SALE_STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('quotation', _('Quotation')),
        ('confirmed', _('Confirmed')),
        ('paid', _('Paid')),
        ('partial', _('Partial')),
        ('cancelled', _('Cancelled')),
        ('returned', _('Returned')),
    ]
    
    SALE_TYPE_CHOICES = [
        ('retail', _('Retail')),
        ('wholesale', _('Wholesale')),
        ('online', _('Online')),
        ('phone', _('Phone Order')),
        ('repair', _('Repair Sale')),
    ]
    
    sale_number = models.CharField(_('Sale Number'), max_length=50, unique=True, db_index=True)
    sale_type = models.CharField(_('Sale Type'), max_length=20, choices=SALE_TYPE_CHOICES, default='retail')
    status = models.CharField(_('Status'), max_length=20, choices=SALE_STATUS_CHOICES, default='draft')
    
    customer = models.ForeignKey('crm.Customer', on_delete=models.SET_NULL, null=True, blank=True, related_name='sales', verbose_name=_('Customer'))
    cash_register = models.ForeignKey(CashRegister, on_delete=models.SET_NULL, null=True, blank=True, related_name='sales', verbose_name=_('Cash Register'))
    
    subtotal = CurrencyField(_('Subtotal'), default=0.00)
    discount = CurrencyField(_('Discount'), default=0.00)
    tax_amount = CurrencyField(_('Tax Amount'), default=0.00)
    total_amount = CurrencyField(_('Total Amount'), default=0.00)
    amount_paid = CurrencyField(_('Amount Paid'), default=0.00)
    balance = CurrencyField(_('Balance'), default=0.00)
    
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True, related_name='sales', verbose_name=_('Payment Method'))
    payment_reference = models.CharField(_('Payment Reference'), max_length=100, blank=True, null=True)
    payment_status = models.CharField(_('Payment Status'), max_length=20, choices=[('pending', 'Pending'), ('paid', 'Paid'), ('partial', 'Partial'), ('failed', 'Failed'), ('refunded', 'Refunded')], default='pending')
    
    is_credit = models.BooleanField(_('Credit Sale'), default=False)
    credit_days = models.PositiveIntegerField(_('Credit Days'), default=0)
    due_date = models.DateField(_('Due Date'), blank=True, null=True)
    
    is_invoice = models.BooleanField(_('Create Invoice'), default=False)
    invoice_number = models.CharField(_('Invoice Number'), max_length=50, blank=True, null=True)
    
    sold_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='sales_made', verbose_name=_('Sold By'))
    
    class Meta:
        verbose_name = _('Sale')
        verbose_name_plural = _('Sales')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['sale_number']),
            models.Index(fields=['customer']),
            models.Index(fields=['status']),
            models.Index(fields=['sale_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.sale_number} - {self.total_amount}"
    
    @property
    def display_name(self):
        return f"{self.sale_number} - {self.customer.full_name if self.customer else 'Walk-in'}"
    
    @property
    def is_paid(self):
        return self.payment_status == 'paid' or (self.balance <= 0 and self.total_amount > 0)
    
    @property
    def is_overdue(self):
        from django.utils import timezone
        if self.due_date:
            return self.due_date < timezone.now().date() and self.balance > 0
        return False
    
    def calculate_totals(self):
        """Calculate sale totals from items."""
        from django.db.models import Sum
        items_total = self.items.aggregate(total=Sum('total_price'))['total'] or 0
        self.subtotal = items_total
        self.total_amount = items_total - self.discount + self.tax_amount
        self.balance = self.total_amount - self.amount_paid
        self.save()


class SaleItem(UUIDModel, TimeStampedModel):
    """Items in a sale"""
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items', verbose_name=_('Sale'))
    product = models.ForeignKey('inventory.Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='sale_items', verbose_name=_('Product'))
    service = models.ForeignKey('inventory.Service', on_delete=models.SET_NULL, null=True, blank=True, related_name='sale_items', verbose_name=_('Service'))
    
    product_name = models.CharField(_('Product Name'), max_length=200)
    product_code = models.CharField(_('Product Code'), max_length=50, blank=True, null=True)
    
    quantity = models.DecimalField(_('Quantity'), max_digits=10, decimal_places=3, default=1.000)
    unit_price = CurrencyField(_('Unit Price'), default=0.00)
    total_price = CurrencyField(_('Total Price'), default=0.00)
    
    discount = CurrencyField(_('Discount'), default=0.00)
    tax_rate = models.DecimalField(_('Tax Rate %'), max_digits=5, decimal_places=2, default=0.00)
    tax_amount = CurrencyField(_('Tax Amount'), default=0.00)
    
    serial_number = models.CharField(_('Serial Number'), max_length=100, blank=True, null=True)
    
    notes = models.TextField(_('Notes'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('Sale Item')
        verbose_name_plural = _('Sale Items')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.product_name} - {self.quantity}"
    
    def save(self, *args, **kwargs):
        """Calculate total price before saving."""
        self.total_price = self.quantity * self.unit_price
        self.tax_amount = self.total_price * (self.tax_rate / 100)
        super().save(*args, **kwargs)


class SalePayment(UUIDModel, TimeStampedModel):
    """Payments for a sale"""
    PAYMENT_STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
        ('refunded', _('Refunded')),
    ]
    
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='payments', verbose_name=_('Sale'))
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True, related_name='sale_payments', verbose_name=_('Payment Method'))
    
    amount = CurrencyField(_('Amount'), default=0.00)
    reference = models.CharField(_('Reference'), max_length=100, blank=True, null=True)
    transaction_id = models.CharField(_('Transaction ID'), max_length=100, blank=True, null=True)
    status = models.CharField(_('Status'), max_length=20, choices=PAYMENT_STATUS_CHOICES, default='completed')
    
    payment_date = models.DateTimeField(_('Payment Date'), auto_now_add=True)
    processed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_payments', verbose_name=_('Processed By'))
    
    notes = models.TextField(_('Notes'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('Sale Payment')
        verbose_name_plural = _('Sale Payments')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.sale.sale_number} - {self.amount}"


class Receipt(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """Receipt for a sale"""
    RECEIPT_TYPE_CHOICES = [
        ('thermal', _('Thermal')),
        ('a4', _('A4')),
        ('email', _('Email')),
    ]
    
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE, related_name='receipt', verbose_name=_('Sale'))
    receipt_number = models.CharField(_('Receipt Number'), max_length=50, unique=True)
    receipt_type = models.CharField(_('Receipt Type'), max_length=20, choices=RECEIPT_TYPE_CHOICES, default='thermal')
    
    is_printed = models.BooleanField(_('Printed'), default=False)
    printed_at = models.DateTimeField(_('Printed At'), blank=True, null=True)
    printed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='printed_receipts', verbose_name=_('Printed By'))
    
    is_emailed = models.BooleanField(_('Emailed'), default=False)
    emailed_at = models.DateTimeField(_('Emailed At'), blank=True, null=True)
    
    template = models.CharField(_('Template'), max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = _('Receipt')
        verbose_name_plural = _('Receipts')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.receipt_number} - {self.sale.sale_number}"


class Refund(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """Refund for a sale"""
    REFUND_REASON_CHOICES = [
        ('defective', _('Defective Product')),
        ('wrong_item', _('Wrong Item')),
        ('customer_request', _('Customer Request')),
        ('other', _('Other')),
    ]
    
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='refunds', verbose_name=_('Sale'))
    refund_number = models.CharField(_('Refund Number'), max_length=50, unique=True)
    
    reason = models.CharField(_('Reason'), max_length=20, choices=REFUND_REASON_CHOICES, default='other')
    amount = CurrencyField(_('Amount'), default=0.00)
    
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True, related_name='refunds', verbose_name=_('Payment Method'))
    reference = models.CharField(_('Reference'), max_length=100, blank=True, null=True)
    
    status = models.CharField(_('Status'), max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('completed', 'Completed')], default='pending')
    
    requested_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='requested_refunds', verbose_name=_('Requested By'))
    approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_refunds', verbose_name=_('Approved By'))
    processed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_refunds', verbose_name=_('Processed By'))
    
    requested_at = models.DateTimeField(_('Requested At'), auto_now_add=True)
    approved_at = models.DateTimeField(_('Approved At'), blank=True, null=True)
    processed_at = models.DateTimeField(_('Processed At'), blank=True, null=True)
    
    notes = models.TextField(_('Notes'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('Refund')
        verbose_name_plural = _('Refunds')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.refund_number} - {self.sale.sale_number}"


class RefundItem(UUIDModel, TimeStampedModel):
    """Items in a refund"""
    refund = models.ForeignKey(Refund, on_delete=models.CASCADE, related_name='items', verbose_name=_('Refund'))
    sale_item = models.ForeignKey(SaleItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='refund_items', verbose_name=_('Sale Item'))
    
    product_name = models.CharField(_('Product Name'), max_length=200)
    quantity = models.DecimalField(_('Quantity'), max_digits=10, decimal_places=3, default=1.000)
    unit_price = CurrencyField(_('Unit Price'), default=0.00)
    total_price = CurrencyField(_('Total Price'), default=0.00)
    
    reason = models.TextField(_('Reason'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('Refund Item')
        verbose_name_plural = _('Refund Items')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.product_name} - {self.quantity}"


class POSSession(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """POS session for tracking user sessions"""
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='pos_sessions', verbose_name=_('User'))
    cash_register = models.ForeignKey(CashRegister, on_delete=models.CASCADE, related_name='sessions', verbose_name=_('Cash Register'))
    
    session_key = models.CharField(_('Session Key'), max_length=100, unique=True)
    
    started_at = models.DateTimeField(_('Started At'), auto_now_add=True)
    ended_at = models.DateTimeField(_('Ended At'), blank=True, null=True)
    
    initial_amount = CurrencyField(_('Initial Amount'), default=0.00)
    final_amount = CurrencyField(_('Final Amount'), default=0.00)
    
    total_sales = CurrencyField(_('Total Sales'), default=0.00)
    total_refunds = CurrencyField(_('Total Refunds'), default=0.00)
    total_collected = CurrencyField(_('Total Collected'), default=0.00)
    
    is_active = models.BooleanField(_('Active'), default=True)
    
    class Meta:
        verbose_name = _('POS Session')
        verbose_name_plural = _('POS Sessions')
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.cash_register.name}"


class POSSettings(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """POS settings"""
    receipt_header = models.TextField(_('Receipt Header'), blank=True, null=True)
    receipt_footer = models.TextField(_('Receipt Footer'), blank=True, null=True)
    
    default_payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True, related_name='default_pos_settings', verbose_name=_('Default Payment Method'))
    default_cash_register = models.ForeignKey(CashRegister, on_delete=models.SET_NULL, null=True, blank=True, related_name='default_pos_settings', verbose_name=_('Default Cash Register'))
    
    show_customer_display = models.BooleanField(_('Show Customer Display'), default=True)
    auto_print_receipt = models.BooleanField(_('Auto Print Receipt'), default=True)
    auto_email_receipt = models.BooleanField(_('Auto Email Receipt'), default=False)
    
    tax_included = models.BooleanField(_('Tax Included in Prices'), default=False)
    default_tax_rate = models.DecimalField(_('Default Tax Rate %'), max_digits=5, decimal_places=2, default=0.00)
    
    allow_credit_sales = models.BooleanField(_('Allow Credit Sales'), default=True)
    credit_limit = CurrencyField(_('Credit Limit'), default=0.00)
    
    class Meta:
        verbose_name = _('POS Settings')
        verbose_name_plural = _('POS Settings')
        ordering = ['-created_at']
        unique_together = [['organization', 'branch']]
    
    def __str__(self):
        return f"POS Settings - {self.organization.name} - {self.branch.name}"
