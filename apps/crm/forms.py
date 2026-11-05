"""
Forms for CRM module
"""
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import (
    Customer, Device, CustomerType, CustomerSource,
    CustomerGroup, DeviceBrand, DeviceModel, DeviceCategory,
    CustomerCommunication, CustomerDocument
)


class CustomerForm(forms.ModelForm):
    """Form for creating and updating customers."""
    
    class Meta:
        model = Customer
        fields = [
            'customer_type', 'customer_group', 'source',
            'code', 'first_name', 'last_name', 'company_name',
            'email', 'phone', 'mobile', 'whatsapp',
            'address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country',
            'gender', 'date_of_birth', 'tax_id',
            'status', 'is_verified', 'verification_date',
            'credit_balance', 'loyalty_points',
            'facebook', 'twitter', 'instagram',
            'referred_by', 'referral_code',
            'profile_image', 'notes'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'verification_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        organization = kwargs.pop('organization', None)
        branch = kwargs.pop('branch', None)
        super().__init__(*args, **kwargs)
        
        if organization:
            self.fields['customer_group'].queryset = CustomerGroup.objects.filter(
                organization=organization
            )
        
        if organization:
            self.fields['referred_by'].queryset = Customer.objects.filter(
                organization=organization
            )
    
    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code:
            code = code.upper().strip()
        return code
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            return phone.strip()
        return phone
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            return email.lower().strip()
        return email


class DeviceForm(forms.ModelForm):
    """Form for creating and updating devices."""
    
    class Meta:
        model = Device
        fields = [
            'customer', 'category', 'brand', 'model',
            'name', 'serial_number', 'imei_1', 'imei_2', 'mac_address',
            'color', 'storage', 'ram', 'os_version',
            'purchase_date', 'purchase_price', 'warranty_expiry',
            'status', 'is_active',
            'front_image', 'back_image', 'tag', 'notes'
        ]
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'warranty_expiry': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        organization = kwargs.pop('organization', None)
        branch = kwargs.pop('branch', None)
        super().__init__(*args, **kwargs)
        
        if organization:
            self.fields['customer'].queryset = Customer.objects.filter(
                organization=organization
            )


class CustomerTypeForm(forms.ModelForm):
    """Form for creating and updating customer types."""
    
    class Meta:
        model = CustomerType
        fields = ['name', 'code', 'description', 'is_active', 'color']


class CustomerSourceForm(forms.ModelForm):
    """Form for creating and updating customer sources."""
    
    class Meta:
        model = CustomerSource
        fields = ['name', 'code', 'description', 'is_active']


class CustomerGroupForm(forms.ModelForm):
    """Form for creating and updating customer groups."""
    
    class Meta:
        model = CustomerGroup
        fields = [
            'name', 'code', 'description',
            'discount_percentage', 'credit_limit', 'is_active'
        ]
    
    def __init__(self, *args, **kwargs):
        organization = kwargs.pop('organization', None)
        branch = kwargs.pop('branch', None)
        super().__init__(*args, **kwargs)
        
        if organization:
            self.fields['organization'].initial = organization
            self.fields['organization'].disabled = True
        if branch:
            self.fields['branch'].initial = branch
            self.fields['branch'].disabled = True


class DeviceBrandForm(forms.ModelForm):
    """Form for creating and updating device brands."""
    
    class Meta:
        model = DeviceBrand
        fields = ['name', 'code', 'logo', 'website', 'description', 'is_active']


class DeviceModelForm(forms.ModelForm):
    """Form for creating and updating device models."""
    
    class Meta:
        model = DeviceModel
        fields = ['brand', 'name', 'code', 'image', 'specifications', 'is_active']
        widgets = {
            'specifications': forms.Textarea(attrs={'rows': 5}),
        }


class DeviceCategoryForm(forms.ModelForm):
    """Form for creating and updating device categories."""
    
    class Meta:
        model = DeviceCategory
        fields = ['name', 'code', 'icon', 'description', 'is_active']


class CustomerCommunicationForm(forms.ModelForm):
    """Form for creating and updating customer communications."""
    
    class Meta:
        model = CustomerCommunication
        fields = [
            'customer', 'communication_type', 'direction',
            'subject', 'message', 'response',
            'related_to', 'status',
            'follow_up_required', 'follow_up_date', 'assigned_to'
        ]
        widgets = {
            'follow_up_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'message': forms.Textarea(attrs={'rows': 5}),
            'response': forms.Textarea(attrs={'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        organization = kwargs.pop('organization', None)
        branch = kwargs.pop('branch', None)
        super().__init__(*args, **kwargs)
        
        if organization:
            self.fields['customer'].queryset = Customer.objects.filter(
                organization=organization
            )
            self.fields['assigned_to'].queryset = self.fields['assigned_to'].queryset.filter(
                organization=organization
            )


class CustomerDocumentForm(forms.ModelForm):
    """Form for creating and updating customer documents."""
    
    class Meta:
        model = CustomerDocument
        fields = [
            'customer', 'document_type', 'title',
            'file', 'description', 'expiry_date', 'is_verified'
        ]
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        organization = kwargs.pop('organization', None)
        branch = kwargs.pop('branch', None)
        super().__init__(*args, **kwargs)
        
        if organization:
            self.fields['customer'].queryset = Customer.objects.filter(
                organization=organization
            )


# Quick forms for inline creation
class QuickCustomerForm(forms.ModelForm):
    """Simplified form for quick customer creation."""
    
    class Meta:
        model = Customer
        fields = ['code', 'first_name', 'last_name', 'phone', 'mobile', 'email', 'address_line_1']
        widgets = {
            'address_line_1': forms.TextInput(attrs={'placeholder': 'Address'}),
        }


class QuickDeviceForm(forms.ModelForm):
    """Simplified form for quick device creation."""
    
    class Meta:
        model = Device
        fields = ['name', 'imei_1', 'imei_2', 'serial_number', 'model', 'brand']
