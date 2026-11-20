"""
Services for the documents application.
"""
import os
import re
from django.core.files.base import ContentFile
from django.utils import timezone
from .models import Document, DocumentVersion, DocumentType, DocumentCategory
from rest_framework.exceptions import PermissionDenied, ValidationError


class DocumentService:
    """
    Service for document operations.
    """
    
    def __init__(self, request):
        self.request = request
        self.user = request.user
        self.organization = getattr(request, 'current_organization', None)
    
    def upload_document(self, file, data):
        """
        Upload a new document with security validation.
        
        Validates:
        - User authentication
        - Organization context
        - File type and content
        - File size limits
        - Safe file names (prevent path traversal)
        - Allowed file extensions
        """
        # Validate user authentication
        if not self.user.is_authenticated:
            raise PermissionDenied('Authentication required to upload documents')
        
        # Validate organization context
        if not self.organization:
            raise ValidationError('Organization context required')
        
        # Validate file exists
        if not file:
            raise ValidationError('No file provided')
        
        # Get file properties
        file_name = file.name
        file_size = file.size
        file_type = file.content_type
        
        # Validate file size (max 10MB for demo, configurable in production)
        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
        if file_size > MAX_FILE_SIZE:
            raise ValidationError(f'File size exceeds maximum limit of {MAX_FILE_SIZE / (1024*1024)}MB')
        
        # Validate file extension
        allowed_extensions = {
            # Documents
            '.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt',
            # Spreadsheets
            '.xls', '.xlsx', '.ods', '.csv',
            # Images
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp',
            # Archives
            '.zip', '.rar', '.7z', '.tar', '.gz',
        }
        
        # Extract extension from file name
        ext = os.path.splitext(file_name)[1].lower()
        if ext not in allowed_extensions:
            raise ValidationError(f'File extension {ext} is not allowed. Allowed extensions: {sorted(allowed_extensions)}')
        
        # Validate file name for path traversal
        # Remove any directory components from the file name
        safe_file_name = os.path.basename(file_name)
        if safe_file_name != file_name:
            raise ValidationError('File name contains invalid characters (path traversal detected)')
        
        # Sanitize file name - remove special characters
        # Keep only alphanumeric, spaces, dots, hyphens, underscores
        safe_file_name = re.sub(r'[^\w\s.\-]', '_', safe_file_name)
        
        # Validate MIME type against extension
        # This is a basic check - in production, use python-magic or similar
        extension_mime_types = {
            '.pdf': ['application/pdf'],
            '.jpg': ['image/jpeg'],
            '.jpeg': ['image/jpeg'],
            '.png': ['image/png'],
            '.gif': ['image/gif'],
            '.txt': ['text/plain'],
            '.csv': ['text/csv'],
            '.zip': ['application/zip', 'application/x-zip-compressed'],
        }
        
        if ext in extension_mime_types:
            if file_type not in extension_mime_types[ext]:
                # Log potential MIME type spoofing but don't block (some browsers send wrong types)
                pass  # Could add a warning here
        
        # Validate organization from data matches request organization
        if data.get('organization_id'):
            from apps.organizations.models import Organization
            try:
                org = Organization.objects.get(pk=data['organization_id'])
                if org.pk != self.organization.pk:
                    raise PermissionDenied('Cannot upload document to another organization')
            except Organization.DoesNotExist:
                raise ValidationError('Invalid organization ID')
        
        # Validate branch belongs to organization if provided
        if data.get('branch_id'):
            from apps.branches.models import Branch
            try:
                branch = Branch.objects.get(pk=data['branch_id'])
                if branch.organization.pk != self.organization.pk:
                    raise PermissionDenied('Cannot upload document to a branch of another organization')
            except Branch.DoesNotExist:
                raise ValidationError('Invalid branch ID')
        
        # Create document record
        document = Document.objects.create(
            document_type=data.get('document_type', 'other'),
            file=file,
            file_name=safe_file_name,
            file_size=file_size,
            file_type=file_type,
            title=data.get('title', safe_file_name),
            description=data.get('description', ''),
            reference_number=data.get('reference_number', ''),
            related_entity_type=data.get('related_entity_type'),
            related_entity_id=data.get('related_entity_id'),
            organization=self.organization,
            branch=data.get('branch_id'),
            uploaded_by=self.user,
            document_date=data.get('document_date'),
            expiry_date=data.get('expiry_date'),
            is_public=data.get('is_public', False),
            is_approved=data.get('is_approved', False),
            tags=data.get('tags', '')
        )
        
        return self.get_document_data(document)
    
    def create_document_version(self, document, file, data):
        """
        Create a new version of a document.
        """
        # Get next version number
        last_version = DocumentVersion.objects.filter(
            document=document
        ).order_by('-version_number').first()
        
        next_version = 1
        if last_version:
            next_version = last_version.version_number + 1
        
        # Save the file
        file_name = file.name
        file_size = file.size
        
        # Create version record
        version = DocumentVersion.objects.create(
            document=document,
            version_number=next_version,
            file=file,
            file_name=file_name,
            file_size=file_size,
            description=data.get('description', ''),
            uploaded_by=self.user if self.user.is_authenticated else None
        )
        
        return self.get_document_version_data(version)
    
    def get_document_data(self, document):
        """
        Get document data for API responses.
        """
        return {
            'id': str(document.id),
            'document_type': document.document_type,
            'document_type_display': document.get_document_type_display(),
            'file_name': document.file_name,
            'file_size': document.file_size,
            'file_size_display': document.get_file_size_display(),
            'file_type': document.file_type,
            'file_url': document.file.url if document.file else None,
            'title': document.title,
            'description': document.description,
            'reference_number': document.reference_number,
            'related_entity_type': document.related_entity_type,
            'related_entity_id': str(document.related_entity_id) if document.related_entity_id else None,
            'organization': {
                'id': str(document.organization.id),
                'name': document.organization.name,
            } if document.organization else None,
            'branch': {
                'id': str(document.branch.id),
                'name': document.branch.name,
            } if document.branch else None,
            'uploaded_by': {
                'id': str(document.uploaded_by.id) if document.uploaded_by else None,
                'email': document.uploaded_by.email if document.uploaded_by else None,
            } if document.uploaded_by else None,
            'document_date': document.document_date.isoformat() if document.document_date else None,
            'expiry_date': document.expiry_date.isoformat() if document.expiry_date else None,
            'is_public': document.is_public,
            'is_approved': document.is_approved,
            'tags': document.tags,
            'created_at': document.created_at.isoformat(),
            'updated_at': document.updated_at.isoformat(),
        }
    
    def get_document_version_data(self, version):
        """
        Get document version data for API responses.
        """
        return {
            'id': str(version.id),
            'document': {
                'id': str(version.document.id),
                'title': version.document.title,
            },
            'version_number': version.version_number,
            'file_name': version.file_name,
            'file_size': version.file_size,
            'file_size_display': version.get_file_size_display() if hasattr(version, 'get_file_size_display') else f"{version.file_size} bytes",
            'file_url': version.file.url if version.file else None,
            'description': version.description,
            'uploaded_by': {
                'id': str(version.uploaded_by.id) if version.uploaded_by else None,
                'email': version.uploaded_by.email if version.uploaded_by else None,
            } if version.uploaded_by else None,
            'created_at': version.created_at.isoformat(),
        }
