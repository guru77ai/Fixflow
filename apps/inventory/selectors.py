"""
Selectors for the inventory application.
"""
from django.db.models import Q, Sum, F
from .models import (
    Product, ProductCategory, ProductBrand, UnitOfMeasure,
    Warehouse, StockMovement, StockTransfer, StockAdjustment,
    ProductSerialNumber
)


class ProductSelector:
    """
    Selector for product-related queries.
    """
    
    def __init__(self, request=None):
        self.request = request
        self.user = request.user if request else None
    
    def get_product(self, pk):
        """
        Get a product by ID.
        """
        try:
            product = Product.objects.get(pk=pk)
            return self.get_product_data(product)
        except Product.DoesNotExist:
            return None
    
    def get_all_products(self, **filters):
        """
        Get all products with optional filters.
        """
        queryset = Product.objects.all()
        
        # Apply organization filter
        if self.request and hasattr(self.request, 'organization') and self.request.organization:
            queryset = queryset.filter(organization=self.request.organization)
        
        # Apply branch filter
        if self.request and hasattr(self.request, 'branch') and self.request.branch:
            queryset = queryset.filter(branch=self.request.branch)
        
        # Apply filters
        if 'category_id' in filters:
            queryset = queryset.filter(category_id=filters['category_id'])
        
        if 'brand_id' in filters:
            queryset = queryset.filter(brand_id=filters['brand_id'])
        
        if 'warehouse_id' in filters:
            # This would need to join through stock, but products don't have direct warehouse relation
            pass
        
        if 'is_active' in filters:
            queryset = queryset.filter(is_active=filters['is_active'])
        
        if 'search' in filters and filters['search']:
            search = filters['search']
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search) |
                Q(barcode__icontains=search) |
                Q(description__icontains=search)
            )
        
        return [self.get_product_data(product) for product in queryset.order_by('name')]
    
    def get_product_data(self, product):
        """
        Get product data for responses.
        """
        # Get current stock
        stock_movements = StockMovement.objects.filter(product=product)
        current_stock = stock_movements.aggregate(
            total_in=Sum('quantity_in', filter=Q(quantity_in__gt=0)),
            total_out=Sum('quantity_out', filter=Q(quantity_out__gt=0))
        ) if stock_movements.exists() else {'total_in': 0, 'total_out': 0}
        
        current_stock_value = (current_stock['total_in'] or 0) - (current_stock['total_out'] or 0)
        
        return {
            'id': str(product.id),
            'code': product.code,
            'name': product.name,
            'description': product.description,
            'barcode': product.barcode,
            'category': self.get_product_category_data(product.category) if product.category else None,
            'brand': self.get_product_brand_data(product.brand) if product.brand else None,
            'unit': self.get_unit_of_measure_data(product.unit) if product.unit else None,
            'cost_price': str(product.cost_price) if product.cost_price else None,
            'selling_price': str(product.selling_price) if product.selling_price else None,
            'minimum_stock_level': product.minimum_stock_level,
            'current_stock': current_stock_value,
            'is_active': product.is_active,
            'is_serialized': product.is_serialized,
            'created_at': product.created_at,
            'updated_at': product.updated_at,
        }
    
    def get_product_categories(self, **filters):
        """
        Get all product categories.
        """
        queryset = ProductCategory.objects.all()
        
        # Apply organization filter
        if self.request and hasattr(self.request, 'organization') and self.request.organization:
            queryset = queryset.filter(organization=self.request.organization)
        
        if 'is_active' in filters:
            queryset = queryset.filter(is_active=filters['is_active'])
        
        if 'search' in filters and filters['search']:
            search = filters['search']
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search)
            )
        
        return [self.get_product_category_data(category) for category in queryset.order_by('name')]
    
    def get_product_category_data(self, category):
        """
        Get product category data for responses.
        """
        if not category:
            return None
        return {
            'id': str(category.id),
            'name': category.name,
            'code': category.code,
            'description': category.description,
            'parent': self.get_product_category_data(category.parent) if category.parent else None,
            'is_active': category.is_active,
            'created_at': category.created_at,
        }
    
    def get_product_brands(self, **filters):
        """
        Get all product brands.
        """
        queryset = ProductBrand.objects.all()
        
        # Apply organization filter
        if self.request and hasattr(self.request, 'organization') and self.request.organization:
            queryset = queryset.filter(organization=self.request.organization)
        
        if 'is_active' in filters:
            queryset = queryset.filter(is_active=filters['is_active'])
        
        if 'search' in filters and filters['search']:
            search = filters['search']
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search)
            )
        
        return [self.get_product_brand_data(brand) for brand in queryset.order_by('name')]
    
    def get_product_brand_data(self, brand):
        """
        Get product brand data for responses.
        """
        if not brand:
            return None
        return {
            'id': str(brand.id),
            'name': brand.name,
            'code': brand.code,
            'description': brand.description,
            'is_active': brand.is_active,
            'created_at': brand.created_at,
        }
    
    def get_units_of_measure(self, **filters):
        """
        Get all units of measure.
        """
        queryset = UnitOfMeasure.objects.all()
        
        # Apply organization filter
        if self.request and hasattr(self.request, 'organization') and self.request.organization:
            queryset = queryset.filter(organization=self.request.organization)
        
        if 'is_active' in filters:
            queryset = queryset.filter(is_active=filters['is_active'])
        
        if 'search' in filters and filters['search']:
            search = filters['search']
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search)
            )
        
        return [self.get_unit_of_measure_data(unit) for unit in queryset.order_by('name')]
    
    def get_unit_of_measure_data(self, unit):
        """
        Get unit of measure data for responses.
        """
        if not unit:
            return None
        return {
            'id': str(unit.id),
            'name': unit.name,
            'code': unit.code,
            'description': unit.description,
            'is_active': unit.is_active,
            'created_at': unit.created_at,
        }


class WarehouseSelector:
    """
    Selector for warehouse-related queries.
    """
    
    def __init__(self, request=None):
        self.request = request
        self.user = request.user if request else None
        self.product_selector = ProductSelector(request)
    
    def get_warehouse(self, pk):
        """
        Get a warehouse by ID.
        """
        try:
            warehouse = Warehouse.objects.get(pk=pk)
            return self.get_warehouse_data(warehouse)
        except Warehouse.DoesNotExist:
            return None
    
    def get_all_warehouses(self, **filters):
        """
        Get all warehouses with optional filters.
        """
        queryset = Warehouse.objects.all()
        
        # Apply organization filter
        if self.request and hasattr(self.request, 'organization') and self.request.organization:
            queryset = queryset.filter(organization=self.request.organization)
        
        # Apply branch filter
        if self.request and hasattr(self.request, 'branch') and self.request.branch:
            queryset = queryset.filter(branch=self.request.branch)
        
        if 'is_active' in filters:
            queryset = queryset.filter(is_active=filters['is_active'])
        
        if 'search' in filters and filters['search']:
            search = filters['search']
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search)
            )
        
        return [self.get_warehouse_data(warehouse) for warehouse in queryset.order_by('name')]
    
    def get_warehouse_data(self, warehouse):
        """
        Get warehouse data for responses.
        """
        return {
            'id': str(warehouse.id),
            'code': warehouse.code,
            'name': warehouse.name,
            'description': warehouse.description,
            'address': warehouse.address,
            'city': warehouse.city,
            'state': warehouse.state,
            'postal_code': warehouse.postal_code,
            'country': warehouse.country,
            'phone': warehouse.phone,
            'email': warehouse.email,
            'is_active': warehouse.is_active,
            'created_at': warehouse.created_at,
        }


# Module-level instances for backward compatibility
product_selectors = ProductSelector()
warehouse_selectors = WarehouseSelector()
