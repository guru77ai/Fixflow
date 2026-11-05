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
            'color', 'icon', 'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class SupplierForm(forms.ModelForm):
    """Form for creating and updating suppliers."""
    
    class Meta:
        model = Supplier
        fields = [
            'supplier_number', 'name', 'code', 'description',
            'category', 'address', 'city', 'state', 'postal_code', 'country',
            'phone', 'mobile', 'email', 'website',
            'tax_id', 'registration_number',
            'contact_person', 'contact_phone', 'contact_email',
            'payment_terms', 'credit_limit', 'currency',
            'is_active', 'is_approved', 'rating',
            'notes', 'tags',
            'organization', 'branch'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'description': forms.Textarea(attrs={'rows': 3}),
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
            'supplier', 'document_type', 'document_number',
            'file', 'title', 'description',
            'issue_date', 'expiry_date', 'is_active',
            'organization', 'branch'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }
