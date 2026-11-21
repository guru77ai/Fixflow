"""
Services for the suppliers application.
"""
from django.db import transaction
from .models import Supplier, SupplierCategory, SupplierContact, SupplierDocument
from .selectors import SupplierSelector


class SupplierService:
    """
    Service for supplier-related operations.
    """
    
    def __init__(self, request=None):
        self.request = request
        self.selector = SupplierSelector(request)
    
    def create_supplier(self, data):
        """
        Create a new supplier.
        """
        with transaction.atomic():
            # Get or create category
            category = None
            if 'category_id' in data:
                try:
                    category = SupplierCategory.objects.get(pk=data['category_id'])
                except SupplierCategory.DoesNotExist:
                    pass
            
            # Create supplier
            supplier = Supplier.objects.create(
                code=data.get('code', ''),
                name=data.get('name', ''),
                category=category,
                contact_person=data.get('contact_person', ''),
                phone=data.get('phone', ''),
                mobile=data.get('mobile', ''),
                email=data.get('email', ''),
                address=data.get('address', ''),
                city=data.get('city', ''),
                state=data.get('state', ''),
                postal_code=data.get('postal_code', ''),
                country=data.get('country', ''),
                tax_identification_number=data.get('tax_identification_number', ''),
                notes=data.get('notes', ''),
                is_active=data.get('is_active', True),
            )
            
            # Set organization and branch if available
            if self.request and hasattr(self.request, 'organization') and self.request.organization:
                supplier.organization = self.request.organization
            if self.request and hasattr(self.request, 'branch') and self.request.branch:
                supplier.branch = self.request.branch
            supplier.save()
            
            return self.selector.get_supplier_data(supplier)
    
    def update_supplier(self, pk, data):
        """
        Update a supplier.
        """
        with transaction.atomic():
            try:
                supplier = Supplier.objects.get(pk=pk)
                
                # Validate organization
                if self.request and hasattr(self.request, 'organization') and self.request.organization:
                    if supplier.organization != self.request.organization:
                        raise PermissionError("Cannot update supplier from another organization")
                
                # Update fields
                for field in ['code', 'name', 'contact_person', 'phone', 'mobile', 'email',
                             'address', 'city', 'state', 'postal_code', 'country',
                             'tax_identification_number', 'notes', 'is_active']:
                    if field in data:
                        setattr(supplier, field, data[field])
                
                # Update category
                if 'category_id' in data:
                    try:
                        supplier.category = SupplierCategory.objects.get(pk=data['category_id'])
                    except SupplierCategory.DoesNotExist:
                        pass
                
                supplier.save()
                return self.selector.get_supplier_data(supplier)
            except Supplier.DoesNotExist:
                return None
    
    def delete_supplier(self, pk):
        """
        Delete a supplier (soft delete).
        """
        with transaction.atomic():
            try:
                supplier = Supplier.objects.get(pk=pk)
                
                # Validate organization
                if self.request and hasattr(self.request, 'organization') and self.request.organization:
                    if supplier.organization != self.request.organization:
                        raise PermissionError("Cannot delete supplier from another organization")
                
                supplier.is_active = False
                supplier.save()
                return True
            except Supplier.DoesNotExist:
                return False
    
    def create_supplier_category(self, data):
        """
        Create a new supplier category.
        """
        with transaction.atomic():
            category = SupplierCategory.objects.create(
                name=data.get('name', ''),
                code=data.get('code', ''),
                description=data.get('description', ''),
                is_active=data.get('is_active', True),
            )
            
            # Set organization if available
            if self.request and hasattr(self.request, 'organization') and self.request.organization:
                category.organization = self.request.organization
                category.save()
            
            return self.selector.get_supplier_category_data(category)
    
    def create_supplier_contact(self, supplier_id, data):
        """
        Create a new supplier contact.
        """
        with transaction.atomic():
            supplier = Supplier.objects.get(pk=supplier_id)
            
            # Validate organization
            if self.request and hasattr(self.request, 'organization') and self.request.organization:
                if supplier.organization != self.request.organization:
                    raise PermissionError("Cannot add contact to supplier from another organization")
            
            contact = SupplierContact.objects.create(
                supplier=supplier,
                name=data.get('name', ''),
                position=data.get('position', ''),
                phone=data.get('phone', ''),
                mobile=data.get('mobile', ''),
                email=data.get('email', ''),
                is_primary=data.get('is_primary', False),
                notes=data.get('notes', ''),
            )
            
            return self.selector.get_supplier_contact_data(contact)
    
    def create_supplier_document(self, supplier_id, data, file):
        """
        Create a new supplier document.
        """
        with transaction.atomic():
            supplier = Supplier.objects.get(pk=supplier_id)
            
            # Validate organization
            if self.request and hasattr(self.request, 'organization') and self.request.organization:
                if supplier.organization != self.request.organization:
                    raise PermissionError("Cannot add document to supplier from another organization")
            
            document = SupplierDocument.objects.create(
                supplier=supplier,
                document_type=data.get('document_type', ''),
                title=data.get('title', ''),
                file=file,
                notes=data.get('notes', ''),
            )
            
            return self.selector.get_supplier_document_data(document)


# Module-level instance for backward compatibility
supplier_service = SupplierService()
