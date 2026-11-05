"""
CRM Models for FixSoftRepair Pro
Customer Relationship Management module
"""
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator, MinLengthValidator, RegexValidator
from phonenumber_field.modelfields import PhoneNumberField
from apps.core.models import TimeStampedModel, UUIDModel, OrganizationAndBranchScopedModel, NoteModel


class CustomerType(UUIDModel, TimeStampedModel):
    """
    Customer type classification (e.g., Individual, Company, VIP, etc.)
    """
    name = models.CharField(
        _('Name'),
        max_length=100,
        unique=True,
        help_text=_('Type of customer')
    )
    code = models.CharField(
        _('Code'),
        max_length=10,
        unique=True,
        help_text=_('Short code for customer type')
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
    color = models.CharField(
        _('Color'),
        max_length=20,
        blank=True,
        null=True,
        help_text=_('Color for UI representation')
    )
    
    class Meta:
        verbose_name = _('Customer Type')
        verbose_name_plural = _('Customer Types')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class CustomerSource(UUIDModel, TimeStampedModel):
    """
    Customer acquisition source (e.g., Walk-in, Referral, Online, etc.)
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
        verbose_name = _('Customer Source')
        verbose_name_plural = _('Customer Sources')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class CustomerGroup(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """
    Customer grouping for segmentation and targeted marketing
    """
    name = models.CharField(
        _('Name'),
        max_length=100
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
    discount_percentage = models.DecimalField(
        _('Discount %'),
        max_digits=5,
        decimal_places=2,
        default=0.00,
        help_text=_('Default discount percentage for this group')
    )
    credit_limit = models.DecimalField(
        _('Credit Limit'),
        max_digits=19,
        decimal_places=2,
        default=0.00,
        help_text=_('Maximum credit allowed for customers in this group')
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True
    )
    
    class Meta:
        verbose_name = _('Customer Group')
        verbose_name_plural = _('Customer Groups')
        ordering = ['name']
        unique_together = [['organization', 'code']]
    
    def __str__(self):
        return f"{self.name} ({self.organization.name})"


class Customer(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel, NoteModel):
    """
    Customer model for CRM
    """
    CUSTOMER_STATUS_CHOICES = [
        ('active', _('Active')),
        ('inactive', _('Inactive')),
        ('blocked', _('Blocked')),
        ('prospect', _('Prospect')),
        ('vip', _('VIP')),
    ]
    
    GENDER_CHOICES = [
        ('male', _('Male')),
        ('female', _('Female')),
        ('other', _('Other')),
        ('unknown', _('Unknown')),
    ]
    
    customer_type = models.ForeignKey(
        CustomerType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='customers',
        verbose_name=_('Customer Type')
    )
    customer_group = models.ForeignKey(
        CustomerGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='customers',
        verbose_name=_('Customer Group')
    )
    source = models.ForeignKey(
        CustomerSource,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='customers',
        verbose_name=_('Source')
    )
    
    # Basic information
    code = models.CharField(
        _('Code'),
        max_length=20,
        unique=True,
        db_index=True,
        help_text=_('Unique customer code')
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
    company_name = models.CharField(
        _('Company Name'),
        max_length=200,
        blank=True,
        null=True,
        help_text=_('Company name for business customers')
    )
    
    # Contact information
    email = models.EmailField(
        _('Email'),
        blank=True,
        null=True,
        validators=[EmailValidator()]
    )
    phone = PhoneNumberField(
        _('Phone'),
        blank=True,
        null=True,
        help_text=_('Primary phone number')
    )
    mobile = PhoneNumberField(
        _('Mobile'),
        blank=True,
        null=True,
        help_text=_('Mobile phone number')
    )
    whatsapp = PhoneNumberField(
        _('WhatsApp'),
        blank=True,
        null=True,
        help_text=_('WhatsApp number')
    )
    
    # Address information
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
    
    # Personal information
    gender = models.CharField(
        _('Gender'),
        max_length=10,
        choices=GENDER_CHOICES,
        default='unknown'
    )
    date_of_birth = models.DateField(
        _('Date of Birth'),
        blank=True,
        null=True
    )
    tax_id = models.CharField(
        _('Tax ID'),
        max_length=50,
        blank=True,
        null=True,
        help_text=_('Tax identification number')
    )
    
    # Status and metadata
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=CUSTOMER_STATUS_CHOICES,
        default='active'
    )
    is_verified = models.BooleanField(
        _('Verified'),
        default=False,
        help_text=_('Customer identity verified')
    )
    verification_date = models.DateTimeField(
        _('Verification Date'),
        blank=True,
        null=True
    )
    
    # Financial information
    credit_balance = models.DecimalField(
        _('Credit Balance'),
        max_digits=19,
        decimal_places=2,
        default=0.00,
        help_text=_('Current credit balance (positive = owes money, negative = prepaid)')
    )
    total_purchases = models.DecimalField(
        _('Total Purchases'),
        max_digits=19,
        decimal_places=2,
        default=0.00
    )
    total_repairs = models.PositiveIntegerField(
        _('Total Repairs'),
        default=0
    )
    loyalty_points = models.PositiveIntegerField(
        _('Loyalty Points'),
        default=0
    )
    
    # Social media
    facebook = models.URLField(
        _('Facebook'),
        blank=True,
        null=True
    )
    twitter = models.URLField(
        _('Twitter'),
        blank=True,
        null=True
    )
    instagram = models.URLField(
        _('Instagram'),
        blank=True,
        null=True
    )
    
    # Referral information
    referred_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='referrals',
        verbose_name=_('Referred By')
    )
    referral_code = models.CharField(
        _('Referral Code'),
        max_length=20,
        blank=True,
        null=True,
        unique=True
    )
    
    # Image
    profile_image = models.ImageField(
        _('Profile Image'),
        upload_to='customers/profile_images/',
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['phone']),
            models.Index(fields=['email']),
            models.Index(fields=['status']),
            models.Index(fields=['organization', 'code']),
        ]
    
    def __str__(self):
        if self.company_name:
            return f"{self.company_name} ({self.code})"
        return f"{self.first_name} {self.last_name or ''} ({self.code})".strip()
    
    @property
    def full_name(self):
        """Get customer full name."""
        if self.company_name:
            return self.company_name
        return f"{self.first_name} {self.last_name or ''}".strip()
    
    @property
    def primary_phone(self):
        """Get primary phone number."""
        return self.phone or self.mobile
    
    @property
    def display_name(self):
        """Display name for UI."""
        return f"{self.code} - {self.full_name}"
    
    def get_balance(self):
        """Get current balance."""
        return self.credit_balance
    
    def update_credit(self, amount):
        """Update credit balance."""
        self.credit_balance += amount
        self.save(update_fields=['credit_balance'])


class DeviceBrand(UUIDModel, TimeStampedModel):
    """
    Device brand (e.g., Apple, Samsung, Huawei, etc.)
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
    logo = models.ImageField(
        _('Logo'),
        upload_to='device_brands/logos/',
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
        verbose_name = _('Device Brand')
        verbose_name_plural = _('Device Brands')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class DeviceModel(UUIDModel, TimeStampedModel):
    """
    Device model (e.g., iPhone 15, Galaxy S24, etc.)
    """
    brand = models.ForeignKey(
        DeviceBrand,
        on_delete=models.CASCADE,
        related_name='models',
        verbose_name=_('Brand')
    )
    name = models.CharField(
        _('Name'),
        max_length=100
    )
    code = models.CharField(
        _('Code'),
        max_length=20,
        unique=True
    )
    image = models.ImageField(
        _('Image'),
        upload_to='device_models/images/',
        blank=True,
        null=True
    )
    specifications = models.JSONField(
        _('Specifications'),
        blank=True,
        null=True,
        help_text=_('Device specifications in JSON format')
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True
    )
    
    class Meta:
        verbose_name = _('Device Model')
        verbose_name_plural = _('Device Models')
        ordering = ['brand__name', 'name']
        unique_together = [['brand', 'name']]
    
    def __str__(self):
        return f"{self.brand.name} {self.name}"


class DeviceCategory(UUIDModel, TimeStampedModel):
    """
    Device category (e.g., Smartphone, Tablet, Laptop, etc.)
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
    icon = models.CharField(
        _('Icon'),
        max_length=50,
        blank=True,
        null=True,
        help_text=_('Icon class for UI')
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
        verbose_name = _('Device Category')
        verbose_name_plural = _('Device Categories')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Device(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel, NoteModel):
    """
    Customer device registry
    """
    DEVICE_STATUS_CHOICES = [
        ('new', _('New')),
        ('used', _('Used')),
        ('refurbished', _('Refurbished')),
        ('broken', _('Broken')),
        ('lost', _('Lost')),
        ('stolen', _('Stolen')),
    ]
    
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='devices',
        verbose_name=_('Customer')
    )
    category = models.ForeignKey(
        DeviceCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='devices',
        verbose_name=_('Category')
    )
    brand = models.ForeignKey(
        DeviceBrand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='customer_devices',
        verbose_name=_('Brand')
    )
    model = models.ForeignKey(
        DeviceModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='customer_devices',
        verbose_name=_('Model')
    )
    
    # Device identification
    name = models.CharField(
        _('Name'),
        max_length=200,
        help_text=_('Custom name for the device')
    )
    serial_number = models.CharField(
        _('Serial Number'),
        max_length=100,
        blank=True,
        null=True,
        db_index=True
    )
    imei_1 = models.CharField(
        _('IMEI 1'),
        max_length=20,
        blank=True,
        null=True,
        db_index=True,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{15,17}$',
                message=_('IMEI must be 15-17 digits')
            )
        ]
    )
    imei_2 = models.CharField(
        _('IMEI 2'),
        max_length=20,
        blank=True,
        null=True,
        db_index=True,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{15,17}$',
                message=_('IMEI must be 15-17 digits')
            )
        ]
    )
    mac_address = models.CharField(
        _('MAC Address'),
        max_length=20,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$',
                message=_('Invalid MAC address format')
            )
        ]
    )
    
    # Device details
    color = models.CharField(
        _('Color'),
        max_length=50,
        blank=True,
        null=True
    )
    storage = models.CharField(
        _('Storage'),
        max_length=50,
        blank=True,
        null=True,
        help_text=_('Storage capacity (e.g., 128GB, 1TB)')
    )
    ram = models.CharField(
        _('RAM'),
        max_length=50,
        blank=True,
        null=True
    )
    os_version = models.CharField(
        _('OS Version'),
        max_length=50,
        blank=True,
        null=True
    )
    
    # Purchase information
    purchase_date = models.DateField(
        _('Purchase Date'),
        blank=True,
        null=True
    )
    purchase_price = models.DecimalField(
        _('Purchase Price'),
        max_digits=19,
        decimal_places=2,
        blank=True,
        null=True
    )
    warranty_expiry = models.DateField(
        _('Warranty Expiry'),
        blank=True,
        null=True
    )
    
    # Status
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=DEVICE_STATUS_CHOICES,
        default='used'
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True
    )
    
    # Images
    front_image = models.ImageField(
        _('Front Image'),
        upload_to='customer_devices/images/',
        blank=True,
        null=True
    )
    back_image = models.ImageField(
        _('Back Image'),
        upload_to='customer_devices/images/',
        blank=True,
        null=True
    )
    
    # Metadata
    tag = models.CharField(
        _('Tag/ID'),
        max_length=50,
        blank=True,
        null=True,
        help_text=_('Custom tag or ID for the device')
    )
    
    class Meta:
        verbose_name = _('Device')
        verbose_name_plural = _('Devices')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['customer', 'serial_number']),
            models.Index(fields=['customer', 'imei_1']),
            models.Index(fields=['customer', 'imei_2']),
            models.Index(fields=['serial_number']),
            models.Index(fields=['imei_1']),
            models.Index(fields=['imei_2']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.tag or self.id})"
    
    @property
    def display_name(self):
        """Display name with customer."""
        if self.model:
            return f"{self.customer.full_name} - {self.model}"
        return f"{self.customer.full_name} - {self.name}"
    
    def get_imei_list(self):
        """Get all IMEI numbers."""
        imeis = []
        if self.imei_1:
            imeis.append(self.imei_1)
        if self.imei_2:
            imeis.append(self.imei_2)
        return imeis


class CustomerCommunication(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """
    Track all communications with customers
    """
    COMMUNICATION_TYPE_CHOICES = [
        ('phone', _('Phone Call')),
        ('email', _('Email')),
        ('sms', _('SMS')),
        ('whatsapp', _('WhatsApp')),
        ('in_person', _('In Person')),
        ('social_media', _('Social Media')),
        ('other', _('Other')),
    ]
    
    DIRECTION_CHOICES = [
        ('inbound', _('Inbound')),
        ('outbound', _('Outbound')),
    ]
    
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='communications',
        verbose_name=_('Customer')
    )
    communication_type = models.CharField(
        _('Type'),
        max_length=20,
        choices=COMMUNICATION_TYPE_CHOICES
    )
    direction = models.CharField(
        _('Direction'),
        max_length=10,
        choices=DIRECTION_CHOICES,
        default='inbound'
    )
    subject = models.CharField(
        _('Subject'),
        max_length=200
    )
    message = models.TextField(
        _('Message')
    )
    response = models.TextField(
        _('Response'),
        blank=True,
        null=True
    )
    
    # Related to
    related_to = models.CharField(
        _('Related To'),
        max_length=100,
        blank=True,
        null=True,
        help_text=_('What this communication is related to (e.g., Repair #123, Invoice #456)')
    )
    
    # Status
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=[
            ('open', _('Open')),
            ('pending', _('Pending')),
            ('resolved', _('Resolved')),
            ('closed', _('Closed')),
        ],
        default='open'
    )
    
    # Follow-up
    follow_up_required = models.BooleanField(
        _('Follow-up Required'),
        default=False
    )
    follow_up_date = models.DateTimeField(
        _('Follow-up Date'),
        blank=True,
        null=True
    )
    
    # Assigned to
    assigned_to = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_communications',
        verbose_name=_('Assigned To')
    )
    
    class Meta:
        verbose_name = _('Customer Communication')
        verbose_name_plural = _('Customer Communications')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.customer.full_name} - {self.subject}"


class CustomerDocument(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """
    Customer document storage
    """
    DOCUMENT_TYPE_CHOICES = [
        ('id_card', _('ID Card')),
        ('passport', _('Passport')),
        ('driving_license', _('Driving License')),
        ('business_license', _('Business License')),
        ('tax_certificate', _('Tax Certificate')),
        ('contract', _('Contract')),
        ('receipt', _('Receipt')),
        ('warranty', _('Warranty')),
        ('other', _('Other')),
    ]
    
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name=_('Customer')
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
        upload_to='customer_documents/'
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
        verbose_name = _('Customer Document')
        verbose_name_plural = _('Customer Documents')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.customer.full_name} - {self.title}"
