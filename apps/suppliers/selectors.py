"""
Selectors for the suppliers application.
"""
from django.db.models import Q
from .models import Supplier, SupplierCategory, SupplierContact, SupplierDocument


class SupplierSelector:
    """
    Selector for supplier-related queries.
    """
    
    def __init__(self, request=None):
        self.request = request
        self.user = request.user if request else None
    
    def get_supplier(self, pk):
        """
        Get a supplier by ID.
        """
        try:
            supplier = Supplier.objects.get(pk=pk)
            return self.get_supplier_data(supplier)
        except Supplier.DoesNotExist:
            return None
    
    def get_all_suppliers(self, **filters):
        """
        Get all suppliers with optional filters.
        """
        queryset = Supplier.objects.all()
        
        # Apply organization filter
        if self.request and hasattr(self.request, 'organization') and self.request.organization:
            queryset = queryset.filter(organization=self.request.organization)
        
        # Apply branch filter
        if self.request and hasattr(self.request, 'branch') and self.request.branch:
            queryset = queryset.filter(branch=self.request.branch)
        
        # Apply filters
        if 'is_active' in filters:
            queryset = queryset.filter(is_active=filters['is_active'])
        
        if 'category_id' in filters:
            queryset = queryset.filter(category_id=filters['category_id'])
        
        if 'search' in filters and filters['search']:
            search = filters['search']
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search) |
                Q(phone__icontains=search) |
                Q(email__icontains=search)
            )
        
        return [self.get_supplier_data(supplier) for supplier in queryset.order_by('name')]
    
    def get_supplier_data(self, supplier):
        """
        Get supplier data for responses.
        """
        return {
            'id': str(supplier.id),
            'code': supplier.code,
            'name': supplier.name,
            'category': self.get_supplier_category_data(supplier.category) if supplier.category else None,
            'contact_person': supplier.contact_person,
            'phone': supplier.phone,
            'mobile': supplier.mobile,
            'email': supplier.email,
            'address': supplier.address,
            'city': supplier.city,
            'state': supplier.state,
            'postal_code': supplier.postal_code,
            'country': supplier.country,
            'tax_identification_number': supplier.tax_identification_number,
            'notes': supplier.notes,
            'is_active': supplier.is_active,
            'created_at': supplier.created_at,
            'updated_at': supplier.updated_at,
        }
    
    def get_supplier_categories(self, **filters):
        """
        Get all supplier categories.
        """
        queryset = SupplierCategory.objects.all()
        
        if 'is_active' in filters:
            queryset = queryset.filter(is_active=filters['is_active'])
        
        if 'search' in filters and filters['search']:
            search = filters['search']
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search)
            )
        
        return [self.get_supplier_category_data(category) for category in queryset.order_by('name')]
    
    def get_supplier_category_data(self, category):
        """
        Get supplier category data for responses.
        """
        if not category:
            return None
        return {
            'id': str(category.id),
            'name': category.name,
            'code': category.code,
            'description': category.description,
            'is_active': category.is_active,
            'created_at': category.created_at,
        }
    
    def get_supplier_contacts(self, supplier_id, **filters):
        """
        Get contacts for a supplier.
        """
        queryset = SupplierContact.objects.filter(supplier_id=supplier_id)
        
        if 'is_primary' in filters:
            queryset = queryset.filter(is_primary=filters['is_primary'])
        
        return [self.get_supplier_contact_data(contact) for contact in queryset.order_by('-is_primary', 'name')]
    
    def get_supplier_contact_data(self, contact):
        """
        Get supplier contact data for responses.
        """
        return {
            'id': str(contact.id),
            'supplier_id': str(contact.supplier_id),
            'name': contact.name,
            'position': contact.position,
            'phone': contact.phone,
            'mobile': contact.mobile,
            'email': contact.email,
            'is_primary': contact.is_primary,
            'notes': contact.notes,
            'created_at': contact.created_at,
        }
    
    def get_supplier_documents(self, supplier_id, **filters):
        """
        Get documents for a supplier.
        """
        queryset = SupplierDocument.objects.filter(supplier_id=supplier_id)
        
        return [self.get_supplier_document_data(doc) for doc in queryset.order_by('-created_at')]
    
    def get_supplier_document_data(self, document):
        """
        Get supplier document data for responses.
        """
        return {
            'id': str(document.id),
            'supplier_id': str(document.supplier_id),
            'document_type': document.document_type,
            'title': document.title,
            'file': document.file.url if document.file else None,
            'notes': document.notes,
            'created_at': document.created_at,
        }


# Module-level instance for backward compatibility
supplier_selectors = SupplierSelector()
