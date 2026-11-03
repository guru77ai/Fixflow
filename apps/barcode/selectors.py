"""
Selectors for the barcode application.
"""
from django.db.models import Q
from .models import Barcode, BarcodeTemplate, BarcodeSymbology


class BarcodeSelector:
    """
    Selector for barcode queries.
    """
    
    def __init__(self, request):
        self.request = request
        self.user = request.user
        self.organization = getattr(request, 'current_organization', None)
    
    def get_barcode(self, pk):
        """
        Get a barcode by ID.
        """
        try:
            barcode = Barcode.objects.get(pk=pk)
            
            # Check organization access
            if barcode.organization and not self.has_organization_access(barcode.organization):
                return None
            
            return self.get_barcode_data(barcode)
        except Barcode.DoesNotExist:
            return None
    
    def get_barcodes(self, **filters):
        """
        Get a list of barcodes.
        """
        queryset = Barcode.objects.all()
        
        # Apply organization filter based on user access
        if self.user.is_authenticated:
            if self.user.is_superuser:
                # Superusers can see all barcodes
                pass
            else:
                # Regular users can only see barcodes for their organizations
                from apps.organizations.models import OrganizationMembership
                org_ids = OrganizationMembership.objects.filter(
                    user=self.user
                ).values_list('organization', flat=True)
                queryset = queryset.filter(organization_id__in=org_ids)
        else:
            # Anonymous users can't see any barcodes
            queryset = queryset.none()
        
        # Apply additional filters
        if 'data' in filters:
            queryset = queryset.filter(data__icontains=filters['data'])
        
        if 'symbology' in filters:
            queryset = queryset.filter(symbology=filters['symbology'])
        
        if 'related_entity_type' in filters:
            queryset = queryset.filter(related_entity_type=filters['related_entity_type'])
        
        if 'related_entity_id' in filters:
            queryset = queryset.filter(related_entity_id=filters['related_entity_id'])
        
        if 'is_active' in filters:
            queryset = queryset.filter(is_active=filters['is_active'])
        
        if 'search' in filters and filters['search']:
            search = filters['search']
            queryset = queryset.filter(
                Q(data__icontains=search) |
                Q(related_entity_type__icontains=search)
            )
        
        return [
            self.get_barcode_data(barcode) for barcode in queryset.order_by('-created_at')[:50]
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
    
    def get_barcode_data(self, barcode):
        """
        Get barcode data for responses.
        """
        return {
            'id': str(barcode.id),
            'data': barcode.data,
            'symbology': barcode.symbology,
            'symbology_display': barcode.get_symbology_display(),
            'width': barcode.width,
            'height': barcode.height,
            'show_text': barcode.show_text,
            'text_position': barcode.text_position,
            'related_entity_type': barcode.related_entity_type,
            'related_entity_id': str(barcode.related_entity_id) if barcode.related_entity_id else None,
            'organization': {
                'id': str(barcode.organization.id),
                'name': barcode.organization.name,
            } if barcode.organization else None,
            'branch': {
                'id': str(barcode.branch.id),
                'name': barcode.branch.name,
            } if barcode.branch else None,
            'is_active': barcode.is_active,
            'created_at': barcode.created_at.isoformat(),
        }
    
    def get_barcode_templates(self, **filters):
        """
        Get a list of barcode templates.
        """
        queryset = BarcodeTemplate.objects.all()
        
        # Apply organization filter based on user access
        if self.user.is_authenticated:
            if self.user.is_superuser:
                # Superusers can see all templates
                pass
            else:
                # Regular users can only see templates for their organizations
                from apps.organizations.models import OrganizationMembership
                org_ids = OrganizationMembership.objects.filter(
                    user=self.user
                ).values_list('organization', flat=True)
                queryset = queryset.filter(organization_id__in=org_ids)
        else:
            # Anonymous users can't see any templates
            queryset = queryset.none()
        
        # Apply additional filters
        if 'name' in filters:
            queryset = queryset.filter(name__icontains=filters['name'])
        
        if 'code' in filters:
            queryset = queryset.filter(code__icontains=filters['code'])
        
        if 'symbology' in filters:
            queryset = queryset.filter(symbology=filters['symbology'])
        
        if 'is_active' in filters:
            queryset = queryset.filter(is_active=filters['is_active'])
        
        if 'search' in filters and filters['search']:
            search = filters['search']
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search)
            )
        
        return [
            self.get_barcode_template_data(template) for template in queryset.order_by('name')
        ]
    
    def get_barcode_template(self, pk):
        """
        Get a barcode template by ID.
        """
        try:
            template = BarcodeTemplate.objects.get(pk=pk)
            
            # Check organization access
            if not self.has_organization_access(template.organization):
                return None
            
            return self.get_barcode_template_data(template)
        except BarcodeTemplate.DoesNotExist:
            return None
    
    def get_barcode_template_data(self, template):
        """
        Get barcode template data for responses.
        """
        return {
            'id': str(template.id),
            'name': template.name,
            'code': template.code,
            'symbology': template.symbology,
            'symbology_display': template.get_symbology_display(),
            'width': template.width,
            'height': template.height,
            'show_text': template.show_text,
            'text_position': template.text_position,
            'organization': {
                'id': str(template.organization.id),
                'name': template.organization.name,
            },
            'created_by': {
                'id': str(template.created_by.id) if template.created_by else None,
                'email': template.created_by.email if template.created_by else None,
            } if template.created_by else None,
            'is_active': template.is_active,
            'created_at': template.created_at.isoformat(),
            'updated_at': template.updated_at.isoformat(),
        }
    
    def get_barcode_symbologies(self):
        """
        Get a list of barcode symbologies.
        """
        return [
            {
                'code': symbology.code,
                'name': symbology.name,
                'description': symbology.description,
                'is_active': symbology.is_active,
            }
            for symbology in BarcodeSymbology.objects.filter(is_active=True).order_by('name')
        ]
