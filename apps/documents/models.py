"""
Document models.
"""
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.core.models import TimeStampedModel, UUIDModel


class DocumentType(UUIDModel, TimeStampedModel):
    """
    Document type model.
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
        verbose_name = _('Document Type')
        verbose_name_plural = _('Document Types')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Document(UUIDModel, TimeStampedModel):
    """
    Document model for storing uploaded documents.
    """
    DOCUMENT_TYPES = [
        ('invoice', 'Invoice'),
        ('receipt', 'Receipt'),
        ('contract', 'Contract'),
        ('agreement', 'Agreement'),
        ('certificate', 'Certificate'),
        ('license', 'License'),
        ('report', 'Report'),
        ('other', 'Other'),
    ]
    
    document_type = models.CharField(
        _('Document Type'),
        max_length=50,
        choices=DOCUMENT_TYPES,
        db_index=True
    )
    
    # File information
    file = models.FileField(
        _('File'),
        upload_to='documents/',
    )
    file_name = models.CharField(
        _('File Name'),
        max_length=255
    )
    file_size = models.PositiveIntegerField(
        _('File Size (bytes)'),
        default=0
    )
    file_type = models.CharField(
        _('File Type'),
        max_length=100,
        blank=True,
        null=True
    )
    
    # Document information
    title = models.CharField(
        _('Title'),
        max_length=255
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )
    
    # Reference
    reference_number = models.CharField(
        _('Reference Number'),
        max_length=100,
        blank=True,
        null=True
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
        related_name='documents',
        verbose_name=_('Organization')
    )
    branch = models.ForeignKey(
        'branches.Branch',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents',
        verbose_name=_('Branch')
    )
    
    # User
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='uploaded_documents',
        verbose_name=_('Uploaded By')
    )
    
    # Dates
    document_date = models.DateField(
        _('Document Date'),
        null=True,
        blank=True
    )
    expiry_date = models.DateField(
        _('Expiry Date'),
        null=True,
        blank=True
    )
    
    # Status
    is_public = models.BooleanField(
        _('Public'),
        default=False
    )
    is_approved = models.BooleanField(
        _('Approved'),
        default=False
    )
    
    # Tags
    tags = models.CharField(
        _('Tags'),
        max_length=255,
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.get_document_type_display()})"
    
    def get_file_size_display(self):
        """Get human-readable file size."""
        size_kb = self.file_size / 1024
        if size_kb < 1024:
            return f"{size_kb:.2f} KB"
        
        size_mb = size_kb / 1024
        if size_mb < 1024:
            return f"{size_mb:.2f} MB"
        
        size_gb = size_mb / 1024
        return f"{size_gb:.2f} GB"


class DocumentVersion(UUIDModel, TimeStampedModel):
    """
    Document version model for tracking document revisions.
    """
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='versions',
        verbose_name=_('Document')
    )
    
    version_number = models.PositiveIntegerField(
        _('Version Number')
    )
    
    # File information
    file = models.FileField(
        _('File'),
        upload_to='document_versions/',
    )
    file_name = models.CharField(
        _('File Name'),
        max_length=255
    )
    file_size = models.PositiveIntegerField(
        _('File Size (bytes)'),
        default=0
    )
    
    # Version information
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )
    
    # User
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='document_versions',
        verbose_name=_('Uploaded By')
    )
    
    class Meta:
        verbose_name = _('Document Version')
        verbose_name_plural = _('Document Versions')
        ordering = ['-version_number']
        constraints = [
            models.UniqueConstraint(
                fields=['document', 'version_number'],
                name='unique_document_version'
            )
        ]
    
    def __str__(self):
        return f"{self.document.title} v{self.version_number}"


class DocumentCategory(UUIDModel, TimeStampedModel):
    """
    Document category model.
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
        verbose_name = _('Document Category')
        verbose_name_plural = _('Document Categories')
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['parent', 'code'],
                name='unique_category_code_per_parent'
            )
        ]
    
    def __str__(self):
        return self.name
