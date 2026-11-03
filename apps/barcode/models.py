"""
Barcode models.
"""
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.core.models import TimeStampedModel, UUIDModel


class BarcodeSymbology(UUIDModel, TimeStampedModel):
    """
    Barcode symbology model.
    """
    name = models.CharField(
        _('Name'),
        max_length=100,
        unique=True
    )
    code = models.CharField(
        _('Code'),
        max_length=50,
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
        verbose_name = _('Barcode Symbology')
        verbose_name_plural = _('Barcode Symbologies')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Barcode(UUIDModel, TimeStampedModel):
    """
    Barcode model for generating and storing barcodes.
    """
    SYMBOLOGY_CHOICES = [
        ('code128', 'Code 128'),
        ('code39', 'Code 39'),
        ('code93', 'Code 93'),
        ('ean13', 'EAN-13'),
        ('ean8', 'EAN-8'),
        ('upca', 'UPC-A'),
        ('upce', 'UPC-E'),
        ('qr_code', 'QR Code'),
        ('datamatrix', 'Data Matrix'),
        ('pdf417', 'PDF417'),
    ]
    
    # Barcode data
    data = models.CharField(
        _('Data'),
        max_length=255,
        db_index=True
    )
    symbology = models.CharField(
        _('Symbology'),
        max_length=50,
        choices=SYMBOLOGY_CHOICES,
        default='code128'
    )
    
    # Display settings
    width = models.PositiveIntegerField(
        _('Width (px)'),
        default=200
    )
    height = models.PositiveIntegerField(
        _('Height (px)'),
        default=50
    )
    show_text = models.BooleanField(
        _('Show Text'),
        default=True
    )
    text_position = models.CharField(
        _('Text Position'),
        max_length=20,
        choices=[
            ('top', 'Top'),
            ('bottom', 'Bottom'),
        ],
        default='bottom'
    )
    
    # Related entity
    related_entity_type = models.CharField(
        _('Related Entity Type'),
        max_length=100,
        blank=True,
        null=True
    )
    related_entity_id = models.UUIDField(
        _('Related Entity ID'),
        null=True,
        blank=True
    )
    
    # Organization and branch
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='barcodes',
        verbose_name=_('Organization')
    )
    branch = models.ForeignKey(
        'branches.Branch',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='barcodes',
        verbose_name=_('Branch')
    )
    
    # User
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_barcodes',
        verbose_name=_('Created By')
    )
    
    # Status
    is_active = models.BooleanField(
        _('Active'),
        default=True
    )
    
    class Meta:
        verbose_name = _('Barcode')
        verbose_name_plural = _('Barcodes')
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['organization', 'data', 'symbology'],
                name='unique_barcode_per_organization'
            )
        ]
    
    def __str__(self):
        return f"{self.data} ({self.get_symbology_display()})"
    
    def get_image_url(self):
        """
        Get the URL for the barcode image.
        """
        from django.urls import reverse
        return reverse('barcode:api_generate') + f"?data={self.data}&symbology={self.symbology}"


class BarcodeTemplate(UUIDModel, TimeStampedModel):
    """
    Barcode template model.
    """
    name = models.CharField(
        _('Name'),
        max_length=100
    )
    code = models.CharField(
        _('Code'),
        max_length=50,
        unique=True
    )
    
    # Template settings
    symbology = models.CharField(
        _('Symbology'),
        max_length=50,
        choices=Barcode.SYMBOLOGY_CHOICES,
        default='code128'
    )
    width = models.PositiveIntegerField(
        _('Width (px)'),
        default=200
    )
    height = models.PositiveIntegerField(
        _('Height (px)'),
        default=50
    )
    show_text = models.BooleanField(
        _('Show Text'),
        default=True
    )
    text_position = models.CharField(
        _('Text Position'),
        max_length=20,
        choices=[
            ('top', 'Top'),
            ('bottom', 'Bottom'),
        ],
        default='bottom'
    )
    
    # Organization
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='barcode_templates',
        verbose_name=_('Organization')
    )
    
    # User
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='barcode_templates',
        verbose_name=_('Created By')
    )
    
    # Status
    is_active = models.BooleanField(
        _('Active'),
        default=True
    )
    
    class Meta:
        verbose_name = _('Barcode Template')
        verbose_name_plural = _('Barcode Templates')
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['organization', 'code'],
                name='unique_barcode_template_code_per_organization'
            )
        ]
    
    def __str__(self):
        return self.name
