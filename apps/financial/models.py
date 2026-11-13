"""
Financial Models for FixSoftRepair Pro
Financial Management module
"""
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel, UUIDModel, OrganizationAndBranchScopedModel, NoteModel, CurrencyField


class InvoiceStatus(UUIDModel, TimeStampedModel):
    """Invoice status"""
    name = models.CharField(_('Name'), max_length=50, unique=True)
    code = models.CharField(_('Code'), max_length=10, unique=True)
    is_default = models.BooleanField(_('Default'), default=False)
    is_final = models.BooleanField(_('Final'), default=False)
    sequence = models.PositiveIntegerField(_('Sequence'), default=0)
    
    class Meta:
        verbose_name = _('Invoice Status')
        verbose_name_plural = _('Invoice Statuses')
        ordering = ['sequence']
    
    def __str__(self):
        return self.name


class InvoiceType(UUIDModel, TimeStampedModel):
    """Invoice type"""
    name = models.CharField(_('Name'), max_length=50, unique=True)
    code = models.CharField(_('Code'), max_length=10, unique=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    prefix = models.CharField(_('Prefix'), max_length=10, default='INV')
    
    class Meta:
        verbose_name = _('Invoice Type')
        verbose_name_plural = _('Invoice Types')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Invoice(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel, NoteModel):
    """Invoice model"""
    PAYMENT_STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('partial', _('Partial')),
        ('paid', _('Paid')),
        ('overdue', _('Overdue')),
        ('cancelled', _('Cancelled')),
        ('refunded', _('Refunded')),
    ]
    
    invoice_number = models.CharField(_('Invoice Number'), max_length=50, unique=True, db_index=True)
    invoice_type = models.ForeignKey(InvoiceType, on_delete=models.PROTECT, related_name='invoices', verbose_name=_('Invoice Type'))
    status = models.ForeignKey(InvoiceStatus, on_delete=models.PROTECT, related_name='invoices', verbose_name=_('Status'))
    
    customer = models.ForeignKey('crm.Customer', on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices', verbose_name=_('Customer'))
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices', verbose_name=_('Supplier'))
    
    reference = models.CharField(_('Reference'), max_length=100, blank=True, null=True)
    reference_type = models.CharField(_('Reference Type'), max_length=50, blank=True, null=True)
    
    subtotal = CurrencyField(_('Subtotal'), default=0.00)
    discount = CurrencyField(_('Discount'), default=0.00)
    tax_amount = CurrencyField(_('Tax Amount'), default=0.00)
    total_amount = CurrencyField(_('Total Amount'), default=0.00)
    amount_paid = CurrencyField(_('Amount Paid'), default=0.00)
    balance = CurrencyField(_('Balance'), default=0.00)
    
    payment_status = models.CharField(_('Payment Status'), max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    due_date = models.DateField(_('Due Date'), blank=True, null=True)
    paid_date = models.DateField(_('Paid Date'), blank=True, null=True)
    
    payment_method = models.ForeignKey('pos.PaymentMethod', on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices', verbose_name=_('Payment Method'))
    payment_reference = models.CharField(_('Payment Reference'), max_length=100, blank=True, null=True)
    
    is_recurring = models.BooleanField(_('Recurring'), default=False)
    recurring_frequency = models.CharField(_('Frequency'), max_length=20, blank=True, null=True)
    recurring_end_date = models.DateField(_('Recurring End Date'), blank=True, null=True)
    
    terms = models.TextField(_('Terms'), blank=True, null=True)
    
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_invoices', verbose_name=_('Created By'))
    approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_invoices', verbose_name=_('Approved By'))
    
    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['invoice_number']),
            models.Index(fields=['customer']),
            models.Index(fields=['status']),
            models.Index(fields=['due_date']),
        ]
    
    def __str__(self):
        return f"{self.invoice_number} - {self.total_amount}"


class InvoiceItem(UUIDModel, TimeStampedModel):
    """Items in an invoice"""
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items', verbose_name=_('Invoice'))
    product = models.ForeignKey('inventory.Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='invoice_items', verbose_name=_('Product'))
    service = models.ForeignKey('inventory.Service', on_delete=models.SET_NULL, null=True, blank=True, related_name='invoice_items', verbose_name=_('Service'))
    
    description = models.TextField(_('Description'))
    quantity = models.DecimalField(_('Quantity'), max_digits=10, decimal_places=3, default=1.000)
    unit_price = CurrencyField(_('Unit Price'), default=0.00)
    total_price = CurrencyField(_('Total Price'), default=0.00)
    
    discount = CurrencyField(_('Discount'), default=0.00)
    tax_rate = models.DecimalField(_('Tax Rate %'), max_digits=5, decimal_places=2, default=0.00)
    tax_amount = CurrencyField(_('Tax Amount'), default=0.00)
    
    class Meta:
        verbose_name = _('Invoice Item')
        verbose_name_plural = _('Invoice Items')
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        self.tax_amount = self.total_price * (self.tax_rate / 100)
        super().save(*args, **kwargs)


class InvoicePayment(UUIDModel, TimeStampedModel):
    """Payments for an invoice"""
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='invoice_payments', verbose_name=_('Invoice'))
    amount = CurrencyField(_('Amount'), default=0.00)
    payment_method = models.ForeignKey('pos.PaymentMethod', on_delete=models.SET_NULL, null=True, blank=True, related_name='invoice_payments', verbose_name=_('Payment Method'))
    reference = models.CharField(_('Reference'), max_length=100, blank=True, null=True)
    payment_date = models.DateTimeField(_('Payment Date'), auto_now_add=True)
    processed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_invoice_payments', verbose_name=_('Processed By'))
    notes = models.TextField(_('Notes'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('Invoice Payment')
        verbose_name_plural = _('Invoice Payments')
        ordering = ['-created_at']


class Payment(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """General payment model"""
    PAYMENT_TYPE_CHOICES = [
        ('customer', _('Customer Payment')),
        ('supplier', _('Supplier Payment')),
        ('expense', _('Expense Payment')),
        ('transfer', _('Transfer')),
        ('refund', _('Refund')),
        ('other', _('Other')),
    ]
    
    payment_number = models.CharField(_('Payment Number'), max_length=50, unique=True)
    payment_type = models.CharField(_('Payment Type'), max_length=20, choices=PAYMENT_TYPE_CHOICES, default='customer')
    
    amount = CurrencyField(_('Amount'), default=0.00)
    currency = models.CharField(_('Currency'), max_length=3, default='DZD')
    
    payment_method = models.ForeignKey('pos.PaymentMethod', on_delete=models.SET_NULL, null=True, blank=True, related_name='payments', verbose_name=_('Payment Method'))
    reference = models.CharField(_('Reference'), max_length=100, blank=True, null=True)
    
    customer = models.ForeignKey('crm.Customer', on_delete=models.SET_NULL, null=True, blank=True, related_name='payments', verbose_name=_('Customer'))
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.SET_NULL, null=True, blank=True, related_name='supplier_payments', verbose_name=_('Supplier'))
    
    related_to = models.CharField(_('Related To'), max_length=100, blank=True, null=True)
    related_id = models.UUIDField(_('Related ID'), null=True, blank=True)
    
    status = models.CharField(_('Status'), max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed'), ('cancelled', 'Cancelled')], default='completed')
    
    payment_date = models.DateTimeField(_('Payment Date'), auto_now_add=True)
    processed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='financial_processed_payments', verbose_name=_('Processed By'))
    approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_payments', verbose_name=_('Approved By'))
    
    notes = models.TextField(_('Notes'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['payment_number']),
            models.Index(fields=['payment_type']),
            models.Index(fields=['customer']),
            models.Index(fields=['supplier']),
        ]
    
    def __str__(self):
        return f"{self.payment_number} - {self.amount}"


class ExpenseCategory(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """Expense category"""
    name = models.CharField(_('Name'), max_length=100)
    code = models.CharField(_('Code'), max_length=20, unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', verbose_name=_('Parent Category'))
    description = models.TextField(_('Description'), blank=True, null=True)
    is_active = models.BooleanField(_('Active'), default=True)
    
    class Meta:
        verbose_name = _('Expense Category')
        verbose_name_plural = _('Expense Categories')
        ordering = ['name']
        unique_together = [['organization', 'code']]
    
    def __str__(self):
        return self.name


class Expense(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel, NoteModel):
    """Expense model"""
    EXPENSE_STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('submitted', _('Submitted')),
        ('approved', _('Approved')),
        ('paid', _('Paid')),
        ('rejected', _('Rejected')),
        ('cancelled', _('Cancelled')),
    ]
    
    expense_number = models.CharField(_('Expense Number'), max_length=50, unique=True)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.PROTECT, related_name='expenses', verbose_name=_('Category'))
    status = models.CharField(_('Status'), max_length=20, choices=EXPENSE_STATUS_CHOICES, default='draft')
    
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'), blank=True, null=True)
    
    amount = CurrencyField(_('Amount'), default=0.00)
    tax_amount = CurrencyField(_('Tax Amount'), default=0.00)
    total_amount = CurrencyField(_('Total Amount'), default=0.00)
    
    payment_method = models.ForeignKey('pos.PaymentMethod', on_delete=models.SET_NULL, null=True, blank=True, related_name='expenses', verbose_name=_('Payment Method'))
    payment_reference = models.CharField(_('Payment Reference'), max_length=100, blank=True, null=True)
    
    expense_date = models.DateField(_('Expense Date'))
    paid_date = models.DateField(_('Paid Date'), blank=True, null=True)
    
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.SET_NULL, null=True, blank=True, related_name='expenses', verbose_name=_('Supplier'))
    
    submitted_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='submitted_expenses', verbose_name=_('Submitted By'))
    approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_expenses', verbose_name=_('Approved By'))
    paid_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='paid_expenses', verbose_name=_('Paid By'))
    
    receipt_attached = models.BooleanField(_('Receipt Attached'), default=False)
    receipt_file = models.FileField(_('Receipt File'), upload_to='expense_receipts/', blank=True, null=True)
    
    class Meta:
        verbose_name = _('Expense')
        verbose_name_plural = _('Expenses')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['expense_number']),
            models.Index(fields=['category']),
            models.Index(fields=['status']),
            models.Index(fields=['expense_date']),
        ]
    
    def __str__(self):
        return f"{self.expense_number} - {self.title} - {self.amount}"


class ExpenseAttachment(UUIDModel, TimeStampedModel):
    """Attachments for expenses"""
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='attachments', verbose_name=_('Expense'))
    file = models.FileField(_('File'), upload_to='expense_attachments/')
    title = models.CharField(_('Title'), max_length=200, blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    uploaded_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='uploaded_expense_attachments', verbose_name=_('Uploaded By'))
    
    class Meta:
        verbose_name = _('Expense Attachment')
        verbose_name_plural = _('Expense Attachments')
        ordering = ['-created_at']


class FinancialReport(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """Financial report"""
    REPORT_TYPE_CHOICES = [
        ('daily_sales', _('Daily Sales')),
        ('monthly_sales', _('Monthly Sales')),
        ('yearly_sales', _('Yearly Sales')),
        ('profit_loss', _('Profit & Loss')),
        ('balance_sheet', _('Balance Sheet')),
        ('cash_flow', _('Cash Flow')),
        ('tax_summary', _('Tax Summary')),
        ('custom', _('Custom')),
    ]
    
    name = models.CharField(_('Name'), max_length=200)
    report_type = models.CharField(_('Report Type'), max_length=20, choices=REPORT_TYPE_CHOICES)
    
    start_date = models.DateField(_('Start Date'))
    end_date = models.DateField(_('End Date'))
    
    parameters = models.JSONField(_('Parameters'), blank=True, null=True)
    data = models.JSONField(_('Data'), blank=True, null=True)
    
    generated_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='generated_reports', verbose_name=_('Generated By'))
    
    file = models.FileField(_('File'), upload_to='financial_reports/', blank=True, null=True)
    
    class Meta:
        verbose_name = _('Financial Report')
        verbose_name_plural = _('Financial Reports')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.start_date} to {self.end_date})"
