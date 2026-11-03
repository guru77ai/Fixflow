"""
Selectors for the documents application.
"""
from django.db.models import Q
from .models import Document, DocumentVersion, DocumentType, DocumentCategory


class DocumentSelector:
    """
    Selector for document queries.
    """
    
    def __init__(self, request):
        self.request = request
        self.user = request.user
        self.organization = getattr(request, 'current_organization', None)
    
    def get_document(self, pk):
        """
        Get a document by ID.
        """
        try:
            document = Document.objects.get(pk=pk)
            
            # Check organization access
            if document.organization and not self.has_organization_access(document.organization):
                return None
            
            return self.get_document_data(document)
        except Document.DoesNotExist:
            return None
    
    def get_documents(self, **filters):
        """
        Get a list of documents.
        """
        queryset = Document.objects.all()
        
        # Apply organization filter based on user access
        if self.user.is_authenticated:
            if self.user.is_superuser:
                # Superusers can see all documents
                pass
            else:
                # Regular users can only see documents for their organizations
                from apps.organizations.models import OrganizationMembership
                org_ids = OrganizationMembership.objects.filter(
                    user=self.user
                ).values_list('organization', flat=True)
                queryset = queryset.filter(organization_id__in=org_ids)
        else:
            # Anonymous users can't see any documents
            queryset = queryset.none()
        
        # Apply additional filters
        if 'document_type' in filters:
            queryset = queryset.filter(document_type=filters['document_type'])
        
        if 'related_entity_type' in filters:
            queryset = queryset.filter(related_entity_type=filters['related_entity_type'])
        
        if 'related_entity_id' in filters:
            queryset = queryset.filter(related_entity_id=filters['related_entity_id'])
        
        if 'organization_id' in filters:
            queryset = queryset.filter(organization_id=filters['organization_id'])
        
        if 'branch_id' in filters:
            queryset = queryset.filter(branch_id=filters['branch_id'])
        
        if 'uploaded_by' in filters:
            queryset = queryset.filter(uploaded_by=filters['uploaded_by'])
        
        if 'is_public' in filters:
            queryset = queryset.filter(is_public=filters['is_public'])
        
        if 'is_approved' in filters:
            queryset = queryset.filter(is_approved=filters['is_approved'])
        
        if 'search' in filters and filters['search']:
            search = filters['search']
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(file_name__icontains=search) |
                Q(reference_number__icontains=search) |
                Q(tags__icontains=search)
            )
        
        return [
            self.get_document_data(doc) for doc in queryset.order_by('-created_at')[:50]
        ]
    
    def has_organization_access(self, organization):
        """
        Check if user has access to an organization.
        """
        if not self.user.is_authenticated:
            return False
        
        if self.user.is_superuser:
            return True
        
        from apps.organizations.models import OrganizationMembership
        return OrganizationMembership.objects.filter(
            organization=organization,
            user=self.user
        ).exists()
    
    def get_document_data(self, document):
        """
        Get document data for responses.
        """
        return {
            'id': str(document.id),
            'document_type': document.document_type,
            'document_type_display': document.get_document_type_display(),
            'file_name': document.file_name,
            'file_size': document.file_size,
            'file_size_display': document.get_file_size_display(),
            'file_type': document.file_type,
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
    
    def get_document_versions(self, document_id, **filters):
        """
        Get versions of a document.
        """
        try:
            document = Document.objects.get(pk=document_id)
            
            # Check organization access
            if document.organization and not self.has_organization_access(document.organization):
                return []
            
            queryset = DocumentVersion.objects.filter(document=document)
            
            # Apply filters
            if 'version_number' in filters:
                queryset = queryset.filter(version_number=filters['version_number'])
            
            return [
                self.get_document_version_data(version) for version in queryset.order_by('-version_number')
            ]
        except Document.DoesNotExist:
            return []
    
    def get_document_version_data(self, version):
        """
        Get document version data for responses.
        """
        return {
            'id': str(version.id),
            'version_number': version.version_number,
            'file_name': version.file_name,
            'file_size': version.file_size,
            'description': version.description,
            'uploaded_by': {
                'id': str(version.uploaded_by.id) if version.uploaded_by else None,
                'email': version.uploaded_by.email if version.uploaded_by else None,
            } if version.uploaded_by else None,
            'created_at': version.created_at.isoformat(),
        }
    
    def get_document_types(self):
        """
        Get a list of document types.
        """
        return [
            {
                'code': choice[0],
                'name': choice[1],
            }
            for choice in Document.DOCUMENT_TYPES
        ]
    
    def get_document_categories(self):
        """
        Get a list of document categories.
        """
        return [
            {
                'id': str(category.id),
                'name': category.name,
                'code': category.code,
                'description': category.description,
                'is_active': category.is_active,
            }
            for category in DocumentCategory.objects.filter(is_active=True).order_by('name')
        ]
