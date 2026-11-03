"""
Services for the documents application.
"""
import os
from django.core.files.base import ContentFile
from django.utils import timezone
from .models import Document, DocumentVersion, DocumentType, DocumentCategory


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
        Upload a new document.
        """
        # Save the file
        file_name = file.name
        file_size = file.size
        file_type = file.content_type
        
        # Create document record
        document = Document.objects.create(
            document_type=data.get('document_type', 'other'),
            file=file,
            file_name=file_name,
            file_size=file_size,
            file_type=file_type,
            title=data.get('title', file_name),
            description=data.get('description', ''),
            reference_number=data.get('reference_number', ''),
            related_entity_type=data.get('related_entity_type'),
            related_entity_id=data.get('related_entity_id'),
            organization=self.organization,
            branch=data.get('branch_id'),
            uploaded_by=self.user if self.user.is_authenticated else None,
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
