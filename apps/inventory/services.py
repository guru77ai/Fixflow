"""
Services for the inventory application.
"""
from django.db import transaction
from decimal import Decimal
from .models import (
    Product, ProductCategory, ProductBrand, UnitOfMeasure,
    Warehouse, StockMovement, StockTransfer, StockAdjustment,
    ProductSerialNumber
)
from .selectors import ProductSelector, WarehouseSelector


class ProductService:
    """
    Service for product-related operations.
    """
    
    def __init__(self, request=None):
        self.request = request
        self.selector = ProductSelector(request)
    
    def create_product(self, data):
        """
        Create a new product.
        """
        with transaction.atomic():
            # Get or create category
            category = None
            if 'category_id' in data:
                try:
                    category = ProductCategory.objects.get(pk=data['category_id'])
                except ProductCategory.DoesNotExist:
                    pass
            
            # Get or create brand
            brand = None
            if 'brand_id' in data:
                try:
                    brand = ProductBrand.objects.get(pk=data['brand_id'])
                except ProductBrand.DoesNotExist:
                    pass
            
            # Get or create unit
            unit = None
            if 'unit_id' in data:
                try:
                    unit = UnitOfMeasure.objects.get(pk=data['unit_id'])
                except UnitOfMeasure.DoesNotExist:
                    pass
            
            # Create product
            product = Product.objects.create(
                code=data.get('code', ''),
                name=data.get('name', ''),
                description=data.get('description', ''),
                barcode=data.get('barcode', ''),
                category=category,
                brand=brand,
                unit=unit,
                cost_price=Decimal(data.get('cost_price', '0')) if data.get('cost_price') else None,
                selling_price=Decimal(data.get('selling_price', '0')) if data.get('selling_price') else None,
                minimum_stock_level=data.get('minimum_stock_level', 0),
                is_active=data.get('is_active', True),
                is_serialized=data.get('is_serialized', False),
            )
            
            # Set organization and branch if available
            if self.request and hasattr(self.request, 'organization') and self.request.organization:
                product.organization = self.request.organization
            if self.request and hasattr(self.request, 'branch') and self.request.branch:
                product.branch = self.request.branch
            product.save()
            
            return self.selector.get_product_data(product)
    
    def update_product(self, pk, data):
        """
        Update a product.
        """
        with transaction.atomic():
            try:
                product = Product.objects.get(pk=pk)
                
                # Validate organization
                if self.request and hasattr(self.request, 'organization') and self.request.organization:
                    if product.organization != self.request.organization:
                        raise PermissionError("Cannot update product from another organization")
                
                # Update fields
                for field in ['code', 'name', 'description', 'barcode',
                             'minimum_stock_level', 'is_active', 'is_serialized']:
                    if field in data:
                        setattr(product, field, data[field])
                
                # Update category
                if 'category_id' in data:
                    try:
                        product.category = ProductCategory.objects.get(pk=data['category_id'])
                    except ProductCategory.DoesNotExist:
                        pass
                
                # Update brand
                if 'brand_id' in data:
                    try:
                        product.brand = ProductBrand.objects.get(pk=data['brand_id'])
                    except ProductBrand.DoesNotExist:
                        pass
                
                # Update unit
                if 'unit_id' in data:
                    try:
                        product.unit = UnitOfMeasure.objects.get(pk=data['unit_id'])
                    except UnitOfMeasure.DoesNotExist:
                        pass
                
                # Update prices
                if 'cost_price' in data:
                    product.cost_price = Decimal(data['cost_price']) if data['cost_price'] else None
                if 'selling_price' in data:
                    product.selling_price = Decimal(data['selling_price']) if data['selling_price'] else None
                
                product.save()
                return self.selector.get_product_data(product)
            except Product.DoesNotExist:
                return None
    
    def delete_product(self, pk):
        """
        Delete a product (soft delete).
        """
        with transaction.atomic():
            try:
                product = Product.objects.get(pk=pk)
                
                # Validate organization
                if self.request and hasattr(self.request, 'organization') and self.request.organization:
                    if product.organization != self.request.organization:
                        raise PermissionError("Cannot delete product from another organization")
                
                product.is_active = False
                product.save()
                return True
            except Product.DoesNotExist:
                return False
    
    def create_product_category(self, data):
        """
        Create a new product category.
        """
        with transaction.atomic():
            parent = None
            if 'parent_id' in data:
                try:
                    parent = ProductCategory.objects.get(pk=data['parent_id'])
                except ProductCategory.DoesNotExist:
                    pass
            
            category = ProductCategory.objects.create(
                name=data.get('name', ''),
                code=data.get('code', ''),
                description=data.get('description', ''),
                parent=parent,
                is_active=data.get('is_active', True),
            )
            
            # Set organization if available
            if self.request and hasattr(self.request, 'organization') and self.request.organization:
                category.organization = self.request.organization
                category.save()
            
            return self.selector.get_product_category_data(category)
    
    def create_product_brand(self, data):
        """
        Create a new product brand.
        """
        with transaction.atomic():
            brand = ProductBrand.objects.create(
                name=data.get('name', ''),
                code=data.get('code', ''),
                description=data.get('description', ''),
                is_active=data.get('is_active', True),
            )
            
            # Set organization if available
            if self.request and hasattr(self.request, 'organization') and self.request.organization:
                brand.organization = self.request.organization
                brand.save()
            
            return self.selector.get_product_brand_data(brand)
    
    def create_unit_of_measure(self, data):
        """
        Create a new unit of measure.
        """
        with transaction.atomic():
            unit = UnitOfMeasure.objects.create(
                name=data.get('name', ''),
                code=data.get('code', ''),
                description=data.get('description', ''),
                is_active=data.get('is_active', True),
            )
            
            # Set organization if available
            if self.request and hasattr(self.request, 'organization') and self.request.organization:
                unit.organization = self.request.organization
                unit.save()
            
            return self.selector.get_unit_of_measure_data(unit)


class WarehouseService:
    """
    Service for warehouse-related operations.
    """
    
    def __init__(self, request=None):
        self.request = request
        self.selector = WarehouseSelector(request)
    
    def create_warehouse(self, data):
        """
        Create a new warehouse.
        """
        with transaction.atomic():
            warehouse = Warehouse.objects.create(
                code=data.get('code', ''),
                name=data.get('name', ''),
                description=data.get('description', ''),
                address=data.get('address', ''),
                city=data.get('city', ''),
                state=data.get('state', ''),
                postal_code=data.get('postal_code', ''),
                country=data.get('country', ''),
                phone=data.get('phone', ''),
                email=data.get('email', ''),
                is_active=data.get('is_active', True),
            )
            
            # Set organization and branch if available
            if self.request and hasattr(self.request, 'organization') and self.request.organization:
                warehouse.organization = self.request.organization
            if self.request and hasattr(self.request, 'branch') and self.request.branch:
                warehouse.branch = self.request.branch
            warehouse.save()
            
            return self.selector.get_warehouse_data(warehouse)


# Module-level instances for backward compatibility
product_service = ProductService()
warehouse_service = WarehouseService()
