"""
Forms for Suppliers module
"""
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import SupplierCategory, Supplier, SupplierContact, SupplierDocument


class SupplierCategoryForm(forms.ModelForm):
    """Form for creating and updating supplier categories."""
    
    class Meta:
        model = SupplierCategory
        fields = [
            'name', 'code', 'description',
            'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class SupplierForm(forms.ModelForm):
    """Form for creating and updating suppliers."""
    
    class Meta:
        model = Supplier
        fields = [
            'code', 'name', 'company_name',
            'category', 'email', 'phone', 'mobile', 'website',
            'address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country',
            'tax_id',
            'payment_terms', 'credit_limit', 'credit_balance',
            'status', 'quality_rating', 'delivery_rating',
            'account_manager', 'is_verified', 'is_preferred',
            'notes',
            'organization', 'branch'
        ]
        widgets = {
            'address_line_1': forms.Textarea(attrs={'rows': 3}),
            'address_line_2': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class SupplierContactForm(forms.ModelForm):
    """Form for creating and updating supplier contacts."""
    
    class Meta:
        model = SupplierContact
        fields = [
            'supplier', 'first_name', 'last_name', 'position',
            'email', 'phone', 'mobile',
            'is_primary', 'notes'
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class SupplierDocumentForm(forms.ModelForm):
    """Form for creating and updating supplier documents."""
    
    class Meta:
        model = SupplierDocument
        fields = [
            'supplier', 'document_type',
            'file', 'title', 'description',
            'expiry_date',
            'organization', 'branch'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }
