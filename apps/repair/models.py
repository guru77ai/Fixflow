"""
Repair Models for FixSoftRepair Pro
Repair Management module
"""
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal
from apps.core.models import TimeStampedModel, UUIDModel, OrganizationAndBranchScopedModel, NoteModel, CurrencyField


class RepairStatus(UUIDModel, TimeStampedModel):
    """
    Repair order status (e.g., Received, Diagnosed, In Progress, etc.)
    """
    name = models.CharField(
        _('Name'),
        max_length=100,
        unique=True
    )
    code = models.CharField(
        _('Code'),
        max_length=20,
        unique=True
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )
    color = models.CharField(
        _('Color'),
        max_length=20,
        blank=True,
        null=True,
        help_text=_('Color for UI representation')
    )
    is_initial = models.BooleanField(
        _('Initial Status'),
        default=False,
        help_text=_('Is this the initial status for new repair orders?')
    )
    is_final = models.BooleanField(
        _('Final Status'),
        default=False,
        help_text=_('Is this a final status (cannot be changed)?')
    )
    sequence = models.PositiveIntegerField(
        _('Sequence'),
        default=0,
        help_text=_('Order in which statuses appear')
    )
    
    class Meta:
        verbose_name = _('Repair Status')
        verbose_name_plural = _('Repair Statuses')
        ordering = ['sequence', 'name']
    
    def __str__(self):
        return self.name


class RepairPriority(UUIDModel, TimeStampedModel):
    """
    Repair order priority (e.g., Low, Medium, High, Urgent)
    """
    name = models.CharField(
        _('Name'),
        max_length=50,
        unique=True
    )
    code = models.CharField(
        _('Code'),
        max_length=10,
        unique=True
    )
    level = models.PositiveIntegerField(
        _('Level'),
        default=1,
        help_text=_('Higher level = higher priority')
    )
    color = models.CharField(
        _('Color'),
        max_length=20,
        blank=True,
        null=True
    )
    estimated_hours = models.PositiveIntegerField(
        _('Estimated Hours'),
        default=24,
        help_text=_('Target resolution time in hours')
    )
    
    class Meta:
        verbose_name = _('Repair Priority')
        verbose_name_plural = _('Repair Priorities')
        ordering = ['-level']
    
    def __str__(self):
        return self.name


class RepairCategory(UUIDModel, TimeStampedModel):
    """
    Repair category (e.g., Hardware, Software, Screen, Battery, etc.)
    """
    name = models.CharField(
        _('Name'),
        max_length=100,
        unique=True
    )
    code = models.CharField(
        _('Code'),
        max_length=20,
        unique=True
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('Parent Category')
    )
    icon = models.CharField(
        _('Icon'),
        max_length=50,
        blank=True,
        null=True
    )
    color = models.CharField(
        _('Color'),
        max_length=20,
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True
    )
    
    class Meta:
        verbose_name = _('Repair Category')
        verbose_name_plural = _('Repair Categories')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class RepairType(UUIDModel, TimeStampedModel):
    """
    Repair type (e.g., Screen Replacement, Battery Replacement, etc.)
    """
    name = models.CharField(
        _('Name'),
        max_length=200,
        unique=True
    )
    code = models.CharField(
        _('Code'),
        max_length=20,
        unique=True
    )
    category = models.ForeignKey(
        RepairCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='repair_types',
        verbose_name=_('Category')
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )
    estimated_cost = CurrencyField(
        _('Estimated Cost'),
        blank=True,
        null=True,
        help_text=_('Estimated cost for this repair type')
    )
    estimated_duration = models.PositiveIntegerField(
        _('Estimated Duration (minutes)'),
        default=60,
        help_text=_('Estimated repair duration in minutes')
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True
    )
    
    class Meta:
        verbose_name = _('Repair Type')
        verbose_name_plural = _('Repair Types')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class RepairOrder(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel, NoteModel):
    """
    Main repair order model
    """
    REPAIR_ORDER_TYPE_CHOICES = [
        ('standard', _('Standard Repair')),
        ('express', _('Express Repair')),
        ('warranty', _('Warranty Repair')),
        ('premium', _('Premium Service')),
        ('diagnostic', _('Diagnostic Only')),
    ]
    
    WARRANTY_TYPE_CHOICES = [
        ('none', _('No Warranty')),
        ('standard', _('Standard Warranty')),
        ('extended', _('Extended Warranty')),
        ('lifetime', _('Lifetime Warranty')),
    ]
    
    # Order information
    order_number = models.CharField(
        _('Order Number'),
        max_length=50,
        unique=True,
        db_index=True
    )
    order_type = models.CharField(
        _('Order Type'),
        max_length=20,
        choices=REPAIR_ORDER_TYPE_CHOICES,
        default='standard'
    )
    
    # Customer and device
    customer = models.ForeignKey(
        'crm.Customer',
        on_delete=models.PROTECT,
        related_name='repair_orders',
        verbose_name=_('Customer')
    )
    device = models.ForeignKey(
        'crm.Device',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='repair_orders',
        verbose_name=_('Device')
    )
    
    # Device details (if device is not selected)
    device_name = models.CharField(
        _('Device Name'),
        max_length=200,
        blank=True,
        null=True
    )
    device_imei = models.CharField(
        _('Device IMEI'),
        max_length=20,
        blank=True,
        null=True
    )
    device_serial = models.CharField(
        _('Device Serial'),
        max_length=50,
        blank=True,
        null=True
    )
    device_brand = models.ForeignKey(
        'crm.DeviceBrand',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='repair_orders',
        verbose_name=_('Device Brand')
    )
    device_model = models.ForeignKey(
        'crm.DeviceModel',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='repair_orders',
        verbose_name=_('Device Model')
    )
    
    # Repair details
    repair_type = models.ForeignKey(
        RepairType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='repair_orders',
        verbose_name=_('Repair Type')
    )
    repair_category = models.ForeignKey(
        RepairCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='repair_orders',
        verbose_name=_('Repair Category')
    )
    status = models.ForeignKey(
        RepairStatus,
        on_delete=models.PROTECT,
        related_name='repair_orders',
        verbose_name=_('Status')
    )
    priority = models.ForeignKey(
        RepairPriority,
        on_delete=models.PROTECT,
        default=1,
        related_name='repair_orders',
        verbose_name=_('Priority')
    )
    
    # Issue description
    issue_description = models.TextField(
        _('Issue Description'),
        help_text=_('Detailed description of the problem')
    )
    reported_issue = models.TextField(
        _('Reported Issue'),
        blank=True,
        null=True,
        help_text=_('What the customer reported')
    )
    diagnosis = models.TextField(
        _('Diagnosis'),
        blank=True,
        null=True,
        help_text=_('Technician diagnosis')
    )
    
    # Technician assignment
    assigned_to = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_repairs',
        verbose_name=_('Assigned To')
    )
    
    # Dates
    received_date = models.DateTimeField(
        _('Received Date'),
        auto_now_add=True
    )
    promised_date = models.DateTimeField(
        _('Promised Date'),
        blank=True,
        null=True,
        help_text=_('Date promised to the customer')
    )
    started_date = models.DateTimeField(
        _('Started Date'),
        blank=True,
        null=True
    )
    completed_date = models.DateTimeField(
        _('Completed Date'),
        blank=True,
        null=True
    )
    delivered_date = models.DateTimeField(
        _('Delivered Date'),
        blank=True,
        null=True
    )
    
    # Financial information
    quotation_amount = CurrencyField(
        _('Quotation Amount'),
        default=0.00,
        help_text=_('Amount quoted to the customer')
    )
    labor_cost = CurrencyField(
        _('Labor Cost'),
        default=0.00,
        help_text=_('Labor cost for the repair')
    )
    parts_cost = CurrencyField(
        _('Parts Cost'),
        default=0.00,
        help_text=_('Cost of parts used')
    )
    total_cost = CurrencyField(
        _('Total Cost'),
        default=0.00,
        help_text=_('Total repair cost')
    )
    discount = CurrencyField(
        _('Discount'),
        default=0.00,
        help_text=_('Discount applied')
    )
    tax_amount = CurrencyField(
        _('Tax Amount'),
        default=0.00
    )
    final_amount = CurrencyField(
        _('Final Amount'),
        default=0.00,
        help_text=_('Final amount to be paid')
    )
    amount_paid = CurrencyField(
        _('Amount Paid'),
        default=0.00
    )
    balance = CurrencyField(
        _('Balance'),
        default=0.00,
        help_text=_('Remaining balance to be paid')
    )
    
    # Payment information
    payment_method = models.CharField(
        _('Payment Method'),
        max_length=50,
        blank=True,
        null=True
    )
    payment_status = models.CharField(
        _('Payment Status'),
        max_length=20,
        choices=[
            ('pending', _('Pending')),
            ('partial', _('Partial')),
            ('paid', _('Paid')),
            ('refunded', _('Refunded')),
            ('cancelled', _('Cancelled')),
        ],
        default='pending'
    )
    
    # Warranty
    warranty_type = models.CharField(
        _('Warranty Type'),
        max_length=20,
        choices=WARRANTY_TYPE_CHOICES,
        default='none'
    )
    warranty_period = models.PositiveIntegerField(
        _('Warranty Period (months)'),
        default=0,
        help_text=_('Warranty period in months')
    )
    warranty_expiry = models.DateField(
        _('Warranty Expiry'),
        blank=True,
        null=True
    )
    
    # Internal notes
    internal_notes = models.TextField(
        _('Internal Notes'),
        blank=True,
        null=True,
        help_text=_('Notes visible only to staff')
    )
    customer_notes = models.TextField(
        _('Customer Notes'),
        blank=True,
        null=True,
        help_text=_('Notes to show to the customer')
    )
    
    # Tracking
    is_urgent = models.BooleanField(
        _('Urgent'),
        default=False
    )
    is_warranty_claim = models.BooleanField(
        _('Warranty Claim'),
        default=False
    )
    is_approved = models.BooleanField(
        _('Approved'),
        default=False
    )
    approval_date = models.DateTimeField(
        _('Approval Date'),
        blank=True,
        null=True
    )
    approved_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_repairs',
        verbose_name=_('Approved By')
    )
    
    # Status tracking
    status_changed_at = models.DateTimeField(
        _('Status Changed At'),
        auto_now=True
    )
    status_changed_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='repair_status_changes',
        verbose_name=_('Status Changed By')
    )
    
    # Metadata
    tags = models.JSONField(
        _('Tags'),
        blank=True,
        null=True,
        help_text=_('JSON array of tags')
    )
    
    class Meta:
        verbose_name = _('Repair Order')
        verbose_name_plural = _('Repair Orders')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['customer']),
            models.Index(fields=['device']),
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['assigned_to']),
            models.Index(fields=['order_type']),
            models.Index(fields=['organization', 'order_number']),
            models.Index(fields=['created_at']),
            models.Index(fields=['promised_date']),
        ]
    
    def __str__(self):
        return f"{self.order_number} - {self.customer.full_name}"
    
    @property
    def display_name(self):
        """Display name for UI."""
        device_name = self.device.name if self.device else self.device_name or 'Device'
        return f"{self.order_number} - {device_name} ({self.customer.full_name})"
    
    @property
    def device_display(self):
        """Get device display name."""
        if self.device:
            return str(self.device)
        parts = []
        if self.device_brand:
            parts.append(self.device_brand.name)
        if self.device_model:
            parts.append(self.device_model.name)
        if self.device_name:
            parts.append(self.device_name)
        return ' - '.join(parts) if parts else 'Unknown Device'
    
    @property
    def status_display(self):
        """Get status display with color."""
        return self.status.name
    
    @property
    def priority_display(self):
        """Get priority display."""
        return self.priority.name
    
    @property
    def is_overdue(self):
        """Check if repair is overdue."""
        if self.promised_date:
            from django.utils import timezone
            return self.promised_date < timezone.now() and self.status.code != 'completed'
        return False
    
    @property
    def time_in_status(self):
        """Get time spent in current status."""
        from django.utils import timezone
        if self.status_changed_at:
            return timezone.now() - self.status_changed_at
        return timezone.now() - self.created_at
    
    def calculate_final_amount(self):
        """Calculate final amount based on costs and discount."""
        total = self.labor_cost + self.parts_cost
        total -= self.discount
        total += self.tax_amount
        return total
    
    def update_balance(self):
        """Update balance based on final amount and payments."""
        self.balance = self.final_amount - self.amount_paid
        self.save(update_fields=['balance'])


class RepairOrderHistory(UUIDModel, TimeStampedModel):
    """
    History of changes to repair orders
    """
    repair_order = models.ForeignKey(
        RepairOrder,
        on_delete=models.CASCADE,
        related_name='history',
        verbose_name=_('Repair Order')
    )
    changed_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='repair_history_changes',
        verbose_name=_('Changed By')
    )
    change_type = models.CharField(
        _('Change Type'),
        max_length=50,
        choices=[
            ('status_change', _('Status Change')),
            ('assignment', _('Assignment')),
            ('cost_update', _('Cost Update')),
            ('note_added', _('Note Added')),
            ('approval', _('Approval')),
            ('payment', _('Payment')),
            ('other', _('Other')),
        ]
    )
    field_name = models.CharField(
        _('Field Name'),
        max_length=100,
        blank=True,
        null=True
    )
    old_value = models.TextField(
        _('Old Value'),
        blank=True,
        null=True
    )
    new_value = models.TextField(
        _('New Value'),
        blank=True,
        null=True
    )
    comments = models.TextField(
        _('Comments'),
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('Repair Order History')
        verbose_name_plural = _('Repair Order Histories')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.repair_order.order_number} - {self.change_type}"


class RepairPart(UUIDModel, TimeStampedModel):
    """
    Parts used in a repair
    """
    repair_order = models.ForeignKey(
        RepairOrder,
        on_delete=models.CASCADE,
        related_name='parts',
        verbose_name=_('Repair Order')
    )
    part = models.ForeignKey(
        'inventory.Product',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='repair_parts',
        verbose_name=_('Part')
    )
    part_name = models.CharField(
        _('Part Name'),
        max_length=200
    )
    part_code = models.CharField(
        _('Part Code'),
        max_length=50,
        blank=True,
        null=True
    )
    quantity = models.DecimalField(
        _('Quantity'),
        max_digits=10,
        decimal_places=3,
        default=1.000
    )
    unit_cost = CurrencyField(
        _('Unit Cost'),
        default=0.00
    )
    total_cost = CurrencyField(
        _('Total Cost'),
        default=0.00
    )
    serial_number = models.CharField(
        _('Serial Number'),
        max_length=100,
        blank=True,
        null=True
    )
    is_warranty = models.BooleanField(
        _('Warranty Part'),
        default=False
    )
    notes = models.TextField(
        _('Notes'),
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('Repair Part')
        verbose_name_plural = _('Repair Parts')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.part_name} - {self.repair_order.order_number}"
    
    def save(self, *args, **kwargs):
        """Calculate total cost before saving."""
        self.total_cost = self.quantity * self.unit_cost
        super().save(*args, **kwargs)


class RepairService(UUIDModel, TimeStampedModel):
    """
    Services performed in a repair
    """
    repair_order = models.ForeignKey(
        RepairOrder,
        on_delete=models.CASCADE,
        related_name='services',
        verbose_name=_('Repair Order')
    )
    service = models.ForeignKey(
        'inventory.Service',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='repair_services',
        verbose_name=_('Service')
    )
    service_name = models.CharField(
        _('Service Name'),
        max_length=200
    )
    service_code = models.CharField(
        _('Service Code'),
        max_length=50,
        blank=True,
        null=True
    )
    quantity = models.DecimalField(
        _('Quantity'),
        max_digits=10,
        decimal_places=3,
        default=1.000
    )
    unit_price = CurrencyField(
        _('Unit Price'),
        default=0.00
    )
    total_price = CurrencyField(
        _('Total Price'),
        default=0.00
    )
    duration_minutes = models.PositiveIntegerField(
        _('Duration (minutes)'),
        default=0
    )
    technician = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='repair_services_performed',
        verbose_name=_('Technician')
    )
    notes = models.TextField(
        _('Notes'),
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('Repair Service')
        verbose_name_plural = _('Repair Services')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.service_name} - {self.repair_order.order_number}"
    
    def save(self, *args, **kwargs):
        """Calculate total price before saving."""
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class RepairChecklist(UUIDModel, TimeStampedModel):
    """
    Checklist items for repairs
    """
    repair_order = models.ForeignKey(
        RepairOrder,
        on_delete=models.CASCADE,
        related_name='checklists',
        verbose_name=_('Repair Order')
    )
    item = models.CharField(
        _('Item'),
        max_length=200
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )
    is_completed = models.BooleanField(
        _('Completed'),
        default=False
    )
    completed_at = models.DateTimeField(
        _('Completed At'),
        blank=True,
        null=True
    )
    completed_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='completed_checklists',
        verbose_name=_('Completed By')
    )
    sequence = models.PositiveIntegerField(
        _('Sequence'),
        default=0
    )
    
    class Meta:
        verbose_name = _('Repair Checklist')
        verbose_name_plural = _('Repair Checklists')
        ordering = ['sequence']
    
    def __str__(self):
        return f"{self.item} - {self.repair_order.order_number}"


class RepairAttachment(UUIDModel, TimeStampedModel):
    """
    Attachments for repair orders (photos, documents, etc.)
    """
    repair_order = models.ForeignKey(
        RepairOrder,
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name=_('Repair Order')
    )
    file = models.FileField(
        _('File'),
        upload_to='repair_attachments/'
    )
    file_type = models.CharField(
        _('File Type'),
        max_length=50,
        choices=[
            ('photo', _('Photo')),
            ('document', _('Document')),
            ('video', _('Video')),
            ('other', _('Other')),
        ],
        default='photo'
    )
    title = models.CharField(
        _('Title'),
        max_length=200,
        blank=True,
        null=True
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )
    uploaded_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='uploaded_attachments',
        verbose_name=_('Uploaded By')
    )
    
    class Meta:
        verbose_name = _('Repair Attachment')
        verbose_name_plural = _('Repair Attachments')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title or self.file.name} - {self.repair_order.order_number}"


class RepairTemplate(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """
    Repair templates for common repair types
    """
    name = models.CharField(
        _('Name'),
        max_length=200
    )
    code = models.CharField(
        _('Code'),
        max_length=20,
        unique=True
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )
    repair_type = models.ForeignKey(
        RepairType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='templates',
        verbose_name=_('Repair Type')
    )
    estimated_cost = CurrencyField(
        _('Estimated Cost'),
        default=0.00
    )
    estimated_duration = models.PositiveIntegerField(
        _('Estimated Duration (minutes)'),
        default=60
    )
    checklist_items = models.JSONField(
        _('Checklist Items'),
        blank=True,
        null=True,
        help_text=_('JSON array of checklist items')
    )
    default_parts = models.JSONField(
        _('Default Parts'),
        blank=True,
        null=True,
        help_text=_('JSON array of default parts')
    )
    default_services = models.JSONField(
        _('Default Services'),
        blank=True,
        null=True,
        help_text=_('JSON array of default services')
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True
    )
    
    class Meta:
        verbose_name = _('Repair Template')
        verbose_name_plural = _('Repair Templates')
        ordering = ['name']
        unique_together = [['organization', 'code']]
    
    def __str__(self):
        return self.name
