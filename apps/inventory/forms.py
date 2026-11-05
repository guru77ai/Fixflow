"""
Forms for Inventory module
"""
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import (
    Warehouse, ProductCategory, ProductBrand, UnitOfMeasure,
    Product, ProductSerialNumber, StockMovement, StockTransfer,
    StockAdjustment, Service, ServiceCategory
)


class WarehouseForm(forms.ModelForm):
    """Form for creating and updating warehouses."""
    
    class Meta:
        model = Warehouse
        fields = [
            'name', 'code', 'address', 'phone', 'email',
            'manager', 'is_active', 'is_central',
            'organization', 'branch'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class ProductCategoryForm(forms.ModelForm):
    """Form for creating and updating product categories."""
    
    class Meta:
        model = ProductCategory
        fields = [
            'name', 'code', 'description', 'parent',
            'icon', 'color', 'is_active',
            'organization', 'branch'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class ProductBrandForm(forms.ModelForm):
    """Form for creating and updating product brands."""
    
    class Meta:
        model = ProductBrand
        fields = [
            'name', 'code', 'logo', 'website',
            'description', 'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class UnitOfMeasureForm(forms.ModelForm):
    """Form for creating and updating units of measure."""
    
    class Meta:
        model = UnitOfMeasure
        fields = [
            'name', 'code', 'description', 'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class ProductForm(forms.ModelForm):
    """Form for creating and updating products."""
    
    class Meta:
        model = Product
        fields = [
            'code', 'sku', 'barcode', 'name', 'description',
            'category', 'brand', 'product_type', 'unit',
            'stock_type', 'initial_stock', 'current_stock',
            'minimum_stock', 'maximum_stock',
            'purchase_price', 'selling_price', 'wholesale_price', 'cost_price',
            'tax_rate', 'is_taxable',
            'supplier_code', 'warehouse', 'location',
            'weight', 'dimensions', 'color', 'model', 'part_number',
            'is_serialized', 'is_active', 'is_for_sale', 'is_for_purchase', 'is_for_repair',
            'image', 'tags',
            'organization', 'branch'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'dimensions': forms.TextInput(attrs={'placeholder': 'L x W x H in cm'}),
        }


class ServiceForm(forms.ModelForm):
    """Form for creating and updating services."""
    
    class Meta:
        model = Service
        fields = [
            'code', 'name', 'description', 'category',
            'service_type', 'duration_minutes', 'price',
            'cost', 'is_taxable', 'tax_rate',
            'is_active', 'is_for_sale',
            'organization', 'branch'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class ServiceCategoryForm(forms.ModelForm):
    """Form for creating and updating service categories."""
    
    class Meta:
        model = ServiceCategory
        fields = [
            'name', 'code', 'description', 'parent',
            'icon', 'color', 'is_active',
            'organization', 'branch'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
