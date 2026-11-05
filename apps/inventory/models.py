"""
Inventory Models for FixSoftRepair Pro
Inventory Management module
"""
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal
from apps.core.models import TimeStampedModel, UUIDModel, OrganizationAndBranchScopedModel, NoteModel, CurrencyField


class Warehouse(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """
    Warehouse model for inventory storage locations
    """
    name = models.CharField(
        _('Name'),
        max_length=100
    )
    code = models.CharField(
        _('Code'),
        max_length=20,
        unique=True
    )
    address = models.TextField(
        _('Address'),
        blank=True,
        null=True
    )
    phone = models.CharField(
        _('Phone'),
        max_length=20,
        blank=True,
        null=True
    )
    email = models.EmailField(
        _('Email'),
        blank=True,
        null=True
    )
    manager = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_warehouses',
        verbose_name=_('Manager')
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True
    )
    is_central = models.BooleanField(
        _('Central Warehouse'),
        default=False,
        help_text=_('Is this the central warehouse?')
    )
    
    class Meta:
        verbose_name = _('Warehouse')
        verbose_name_plural = _('Warehouses')
        ordering = ['name']
        unique_together = [['organization', 'code']]
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class ProductCategory(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """
    Product category (e.g., Parts, Accessories, Consumables, etc.)
    """
    name = models.CharField(
        _('Name'),
        max_length=100
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
        verbose_name = _('Product Category')
        verbose_name_plural = _('Product Categories')
        ordering = ['name']
        unique_together = [['organization', 'code']]
    
    def __str__(self):
        return self.name


class ProductBrand(UUIDModel, TimeStampedModel):
    """
    Product brand (e.g., Samsung, Apple, Generic, etc.)
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
    logo = models.ImageField(
        _('Logo'),
        upload_to='product_brands/logos/',
        blank=True,
        null=True
    )
    website = models.URLField(
        _('Website'),
        blank=True,
        null=True
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
        verbose_name = _('Product Brand')
        verbose_name_plural = _('Product Brands')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class UnitOfMeasure(UUIDModel, TimeStampedModel):
    """
    Unit of measure for products (e.g., Piece, Box, Meter, Liter, etc.)
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
        verbose_name = _('Unit of Measure')
        verbose_name_plural = _('Units of Measure')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel, NoteModel):
    """
    Product model for inventory items
    """
    PRODUCT_TYPE_CHOICES = [
        ('part', _('Part')),
        ('accessory', _('Accessory')),
        ('consumable', _('Consumable')),
        ('tool', _('Tool')),
        ('equipment', _('Equipment')),
        ('other', _('Other')),
    ]
    
    STOCK_TYPE_CHOICES = [
        ('serialized', _('Serialized')),
        ('batch', _('Batch Tracked')),
        ('non_serialized', _('Non-Serialized')),
    ]
    
    # Basic information
    code = models.CharField(
        _('Code'),
        max_length=50,
        unique=True,
        db_index=True
    )
    sku = models.CharField(
        _('SKU'),
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        db_index=True
    )
    barcode = models.CharField(
        _('Barcode'),
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        db_index=True
    )
    name = models.CharField(
        _('Name'),
        max_length=200
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )
    
    # Classification
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name=_('Category')
    )
    brand = models.ForeignKey(
        ProductBrand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name=_('Brand')
    )
    product_type = models.CharField(
        _('Product Type'),
        max_length=20,
        choices=PRODUCT_TYPE_CHOICES,
        default='part'
    )
    
    # Unit of measure
    unit = models.ForeignKey(
        UnitOfMeasure,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name=_('Unit of Measure')
    )
    
    # Stock information
    stock_type = models.CharField(
        _('Stock Type'),
        max_length=20,
        choices=STOCK_TYPE_CHOICES,
        default='non_serialized'
    )
    initial_stock = models.DecimalField(
        _('Initial Stock'),
        max_digits=15,
        decimal_places=3,
        default=0.000
    )
    current_stock = models.DecimalField(
        _('Current Stock'),
        max_digits=15,
        decimal_places=3,
        default=0.000
    )
    minimum_stock = models.DecimalField(
        _('Minimum Stock'),
        max_digits=15,
        decimal_places=3,
        default=0.000,
        help_text=_('Minimum stock level for alerts')
    )
    maximum_stock = models.DecimalField(
        _('Maximum Stock'),
        max_digits=15,
        decimal_places=3,
        default=0.000,
        help_text=_('Maximum stock level')
    )
    
    # Pricing
    purchase_price = CurrencyField(
        _('Purchase Price'),
        default=0.00,
        help_text=_('Price at which the product was purchased')
    )
    selling_price = CurrencyField(
        _('Selling Price'),
        default=0.00,
        help_text=_('Price at which the product is sold')
    )
    wholesale_price = CurrencyField(
        _('Wholesale Price'),
        default=0.00,
        blank=True,
        null=True
    )
    cost_price = CurrencyField(
        _('Cost Price'),
        default=0.00,
        help_text=_('Current cost price')
    )
    
    # Tax information
    tax_rate = models.DecimalField(
        _('Tax Rate %'),
        max_digits=5,
        decimal_places=2,
        default=0.00
    )
    is_taxable = models.BooleanField(
        _('Taxable'),
        default=True
    )
    
    # Supplier information (optional, will reference suppliers app when available)
    supplier_code = models.CharField(
        _('Supplier Code'),
        max_length=50,
        blank=True,
        null=True
    )
    
    # Warehouse
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name=_('Warehouse')
    )
    location = models.CharField(
        _('Location'),
        max_length=100,
        blank=True,
        null=True,
        help_text=_('Specific location within the warehouse')
    )
    
    # Product specifications
    weight = models.DecimalField(
        _('Weight (kg)'),
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True
    )
    dimensions = models.CharField(
        _('Dimensions'),
        max_length=100,
        blank=True,
        null=True,
        help_text=_('L x W x H in cm')
    )
    color = models.CharField(
        _('Color'),
        max_length=50,
        blank=True,
        null=True
    )
    model = models.CharField(
        _('Model'),
        max_length=100,
        blank=True,
        null=True
    )
    part_number = models.CharField(
        _('Part Number'),
        max_length=100,
        blank=True,
        null=True
    )
    
    # Serialization
    is_serialized = models.BooleanField(
        _('Serialized'),
        default=False,
        help_text=_('Does this product have unique serial numbers?')
    )
    
    # Status
    is_active = models.BooleanField(
        _('Active'),
        default=True
    )
    is_for_sale = models.BooleanField(
        _('For Sale'),
        default=True
    )
    is_for_purchase = models.BooleanField(
        _('For Purchase'),
        default=True
    )
    is_for_repair = models.BooleanField(
        _('For Repair'),
        default=False,
        help_text=_('Can this product be used in repairs?')
    )
    
    # Images
    image = models.ImageField(
        _('Image'),
        upload_to='products/images/',
        blank=True,
        null=True
    )
    
    # Metadata
    tags = models.JSONField(
        _('Tags'),
        blank=True,
        null=True,
        help_text=_('JSON array of tags')
    )
    
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['sku']),
            models.Index(fields=['barcode']),
            models.Index(fields=['name']),
            models.Index(fields=['category']),
            models.Index(fields=['brand']),
            models.Index(fields=['organization', 'code']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    @property
    def display_name(self):
        """Display name with code."""
        return f"{self.code} - {self.name}"
    
    @property
    def stock_status(self):
        """Get stock status."""
        if self.current_stock <= 0:
            return 'out_of_stock'
        elif self.current_stock <= self.minimum_stock:
            return 'low_stock'
        elif self.current_stock >= self.maximum_stock:
            return 'over_stock'
        else:
            return 'in_stock'
    
    @property
    def stock_value(self):
        """Calculate current stock value."""
        return self.current_stock * self.cost_price
    
    @property
    def profit_margin(self):
        """Calculate profit margin percentage."""
        if self.cost_price > 0:
            return ((self.selling_price - self.cost_price) / self.cost_price) * 100
        return 0
    
    def update_stock(self, quantity, movement_type='in'):
        """Update stock quantity."""
        if movement_type == 'in':
            self.current_stock += quantity
        elif movement_type == 'out':
            self.current_stock -= quantity
        self.save(update_fields=['current_stock'])


class ProductSerialNumber(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """
    Serial numbers for serialized products
    """
    SERIAL_STATUS_CHOICES = [
        ('in_stock', _('In Stock')),
        ('sold', _('Sold')),
        ('used', _('Used in Repair')),
        ('returned', _('Returned')),
        ('defective', _('Defective')),
        ('lost', _('Lost')),
        ('stolen', _('Stolen')),
    ]
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='serial_numbers',
        verbose_name=_('Product')
    )
    serial_number = models.CharField(
        _('Serial Number'),
        max_length=100,
        db_index=True
    )
    batch_number = models.CharField(
        _('Batch Number'),
        max_length=50,
        blank=True,
        null=True
    )
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=SERIAL_STATUS_CHOICES,
        default='in_stock'
    )
    purchase_date = models.DateField(
        _('Purchase Date'),
        blank=True,
        null=True
    )
    purchase_price = CurrencyField(
        _('Purchase Price'),
        default=0.00
    )
    expiry_date = models.DateField(
        _('Expiry Date'),
        blank=True,
        null=True
    )
    location = models.CharField(
        _('Location'),
        max_length=100,
        blank=True,
        null=True
    )
    notes = models.TextField(
        _('Notes'),
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('Product Serial Number')
        verbose_name_plural = _('Product Serial Numbers')
        ordering = ['serial_number']
        unique_together = [['product', 'serial_number']]
        indexes = [
            models.Index(fields=['serial_number']),
            models.Index(fields=['product', 'status']),
        ]
    
    def __str__(self):
        return f"{self.product.code} - {self.serial_number}"


class StockMovement(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """
    Track all stock movements (in, out, transfers, adjustments)
    """
    MOVEMENT_TYPE_CHOICES = [
        ('in', _('Stock In')),
        ('out', _('Stock Out')),
        ('transfer_in', _('Transfer In')),
        ('transfer_out', _('Transfer Out')),
        ('adjustment_plus', _('Adjustment +')),
        ('adjustment_minus', _('Adjustment -')),
        ('return', _('Return')),
        ('damage', _('Damage/Loss')),
    ]
    
    REFERENCE_TYPE_CHOICES = [
        ('purchase', _('Purchase Order')),
        ('sale', _('Sale')),
        ('repair', _('Repair Order')),
        ('transfer', _('Stock Transfer')),
        ('adjustment', _('Stock Adjustment')),
        ('return', _('Return')),
        ('manual', _('Manual Entry')),
        ('other', _('Other')),
    ]
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='stock_movements',
        verbose_name=_('Product')
    )
    movement_type = models.CharField(
        _('Movement Type'),
        max_length=20,
        choices=MOVEMENT_TYPE_CHOICES
    )
    reference_type = models.CharField(
        _('Reference Type'),
        max_length=20,
        choices=REFERENCE_TYPE_CHOICES,
        blank=True,
        null=True
    )
    reference_number = models.CharField(
        _('Reference Number'),
        max_length=100,
        blank=True,
        null=True
    )
    quantity = models.DecimalField(
        _('Quantity'),
        max_digits=15,
        decimal_places=3,
        default=0.000
    )
    unit_cost = CurrencyField(
        _('Unit Cost'),
        default=0.00
    )
    total_cost = CurrencyField(
        _('Total Cost'),
        default=0.00
    )
    
    # Source/Destination
    source_warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stock_movements_out',
        verbose_name=_('Source Warehouse')
    )
    destination_warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stock_movements_in',
        verbose_name=_('Destination Warehouse')
    )
    
    # Related entities
    related_to = models.CharField(
        _('Related To'),
        max_length=100,
        blank=True,
        null=True,
        help_text=_('ID or code of related entity')
    )
    
    # Serial numbers (for serialized products)
    serial_numbers = models.JSONField(
        _('Serial Numbers'),
        blank=True,
        null=True,
        help_text=_('JSON array of serial numbers involved')
    )
    
    # Notes
    notes = models.TextField(
        _('Notes'),
        blank=True,
        null=True
    )
    
    # Performed by
    performed_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stock_movements',
        verbose_name=_('Performed By')
    )
    
    class Meta:
        verbose_name = _('Stock Movement')
        verbose_name_plural = _('Stock Movements')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['movement_type']),
            models.Index(fields=['reference_type']),
            models.Index(fields=['reference_number']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.product.code} - {self.movement_type} - {self.quantity}"
    
    def save(self, *args, **kwargs):
        """Calculate total cost before saving."""
        self.total_cost = self.quantity * self.unit_cost
        super().save(*args, **kwargs)


class StockTransfer(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """
    Stock transfer between warehouses
    """
    TRANSFER_STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('pending', _('Pending')),
        ('in_transit', _('In Transit')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    ]
    
    transfer_number = models.CharField(
        _('Transfer Number'),
        max_length=50,
        unique=True
    )
    source_warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name='stock_transfers_out',
        verbose_name=_('Source Warehouse')
    )
    destination_warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name='stock_transfers_in',
        verbose_name=_('Destination Warehouse')
    )
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=TRANSFER_STATUS_CHOICES,
        default='draft'
    )
    transfer_date = models.DateTimeField(
        _('Transfer Date'),
        blank=True,
        null=True
    )
    received_date = models.DateTimeField(
        _('Received Date'),
        blank=True,
        null=True
    )
    notes = models.TextField(
        _('Notes'),
        blank=True,
        null=True
    )
    
    # Performed by
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_transfers',
        verbose_name=_('Created By')
    )
    received_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='received_transfers',
        verbose_name=_('Received By')
    )
    
    class Meta:
        verbose_name = _('Stock Transfer')
        verbose_name_plural = _('Stock Transfers')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['transfer_number']),
            models.Index(fields=['source_warehouse']),
            models.Index(fields=['destination_warehouse']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.transfer_number} - {self.source_warehouse} -> {self.destination_warehouse}"


class StockTransferItem(UUIDModel, TimeStampedModel):
    """
    Items in a stock transfer
    """
    transfer = models.ForeignKey(
        StockTransfer,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Transfer')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='transfer_items',
        verbose_name=_('Product')
    )
    quantity = models.DecimalField(
        _('Quantity'),
        max_digits=15,
        decimal_places=3,
        default=0.000
    )
    quantity_received = models.DecimalField(
        _('Quantity Received'),
        max_digits=15,
        decimal_places=3,
        default=0.000
    )
    unit_cost = CurrencyField(
        _('Unit Cost'),
        default=0.00
    )
    total_cost = CurrencyField(
        _('Total Cost'),
        default=0.00
    )
    serial_numbers = models.JSONField(
        _('Serial Numbers'),
        blank=True,
        null=True
    )
    notes = models.TextField(
        _('Notes'),
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('Stock Transfer Item')
        verbose_name_plural = _('Stock Transfer Items')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.product.code} - {self.quantity}"
    
    def save(self, *args, **kwargs):
        """Calculate total cost before saving."""
        self.total_cost = self.quantity * self.unit_cost
        super().save(*args, **kwargs)


class StockAdjustment(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """
    Stock adjustment (manual correction)
    """
    ADJUSTMENT_REASON_CHOICES = [
        ('count_error', _('Counting Error')),
        ('damage', _('Damage')),
        ('loss', _('Loss')),
        ('theft', _('Theft')),
        ('found', _('Found')),
        ('other', _('Other')),
    ]
    
    adjustment_number = models.CharField(
        _('Adjustment Number'),
        max_length=50,
        unique=True
    )
    date = models.DateTimeField(
        _('Date'),
        auto_now_add=True
    )
    reason = models.CharField(
        _('Reason'),
        max_length=20,
        choices=ADJUSTMENT_REASON_CHOICES
    )
    notes = models.TextField(
        _('Notes'),
        blank=True,
        null=True
    )
    
    # Performed by
    performed_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stock_adjustments',
        verbose_name=_('Performed By')
    )
    approved_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_adjustments',
        verbose_name=_('Approved By')
    )
    
    class Meta:
        verbose_name = _('Stock Adjustment')
        verbose_name_plural = _('Stock Adjustments')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['adjustment_number']),
            models.Index(fields=['date']),
            models.Index(fields=['reason']),
        ]
    
    def __str__(self):
        return f"{self.adjustment_number} - {self.reason}"


class StockAdjustmentItem(UUIDModel, TimeStampedModel):
    """
    Items in a stock adjustment
    """
    adjustment = models.ForeignKey(
        StockAdjustment,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Adjustment')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='adjustment_items',
        verbose_name=_('Product')
    )
    old_quantity = models.DecimalField(
        _('Old Quantity'),
        max_digits=15,
        decimal_places=3,
        default=0.000
    )
    new_quantity = models.DecimalField(
        _('New Quantity'),
        max_digits=15,
        decimal_places=3,
        default=0.000
    )
    difference = models.DecimalField(
        _('Difference'),
        max_digits=15,
        decimal_places=3,
        default=0.000
    )
    unit_cost = CurrencyField(
        _('Unit Cost'),
        default=0.00
    )
    total_value = CurrencyField(
        _('Total Value'),
        default=0.00
    )
    notes = models.TextField(
        _('Notes'),
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('Stock Adjustment Item')
        verbose_name_plural = _('Stock Adjustment Items')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.product.code} - {self.difference}"
    
    def save(self, *args, **kwargs):
        """Calculate difference and total value before saving."""
        self.difference = self.new_quantity - self.old_quantity
        self.total_value = self.difference * self.unit_cost
        super().save(*args, **kwargs)


class Service(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """
    Service model for sellable services (e.g., Labor, Diagnostic, etc.)
    """
    SERVICE_TYPE_CHOICES = [
        ('labor', _('Labor')),
        ('diagnostic', _('Diagnostic')),
        ('installation', _('Installation')),
        ('maintenance', _('Maintenance')),
        ('consultation', _('Consultation')),
        ('other', _('Other')),
    ]
    
    code = models.CharField(
        _('Code'),
        max_length=20,
        unique=True
    )
    name = models.CharField(
        _('Name'),
        max_length=200
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )
    service_type = models.CharField(
        _('Service Type'),
        max_length=20,
        choices=SERVICE_TYPE_CHOICES,
        default='labor'
    )
    
    # Pricing
    price = CurrencyField(
        _('Price'),
        default=0.00
    )
    cost = CurrencyField(
        _('Cost'),
        default=0.00,
        help_text=_('Cost to provide this service')
    )
    
    # Time
    estimated_duration = models.PositiveIntegerField(
        _('Estimated Duration (minutes)'),
        default=60
    )
    
    # Tax
    tax_rate = models.DecimalField(
        _('Tax Rate %'),
        max_digits=5,
        decimal_places=2,
        default=0.00
    )
    is_taxable = models.BooleanField(
        _('Taxable'),
        default=True
    )
    
    # Status
    is_active = models.BooleanField(
        _('Active'),
        default=True
    )
    
    # Category
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='services',
        verbose_name=_('Category')
    )
    
    # Metadata
    tags = models.JSONField(
        _('Tags'),
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        ordering = ['name']
        unique_together = [['organization', 'code']]
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    @property
    def display_name(self):
        """Display name with code."""
        return f"{self.code} - {self.name}"
    
    @property
    def profit_margin(self):
        """Calculate profit margin percentage."""
        if self.cost > 0:
            return ((self.price - self.cost) / self.cost) * 100
        return 0


class ServiceCategory(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """
    Category for services
    """
    name = models.CharField(
        _('Name'),
        max_length=100
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
    is_active = models.BooleanField(
        _('Active'),
        default=True
    )
    
    class Meta:
        verbose_name = _('Service Category')
        verbose_name_plural = _('Service Categories')
        ordering = ['name']
        unique_together = [['organization', 'code']]
    
    def __str__(self):
        return self.name
