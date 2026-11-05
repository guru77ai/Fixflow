"""
Forms for Repair module
"""
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import (
    RepairOrder, RepairPart, RepairService, RepairChecklist,
    RepairAttachment, RepairTemplate, RepairStatus, RepairPriority,
    RepairCategory, RepairType
)


class RepairOrderForm(forms.ModelForm):
    """Form for creating and updating repair orders."""
    
    class Meta:
        model = RepairOrder
        fields = [
            'order_type', 'customer', 'device',
            'device_name', 'device_imei', 'device_serial', 'device_brand', 'device_model',
            'repair_type', 'repair_category', 'status', 'priority',
            'issue_description', 'reported_issue', 'diagnosis',
            'assigned_to', 'promised_date',
            'quotation_amount', 'labor_cost', 'parts_cost', 'total_cost',
            'discount', 'tax_amount', 'final_amount', 'amount_paid', 'balance',
            'payment_method', 'payment_status',
            'warranty_type', 'warranty_period', 'warranty_expiry',
            'internal_notes', 'customer_notes',
            'is_urgent', 'is_warranty_claim', 'is_approved',
            'approval_date', 'approved_by',
            'tags'
        ]
        widgets = {
            'issue_description': forms.Textarea(attrs={'rows': 5}),
            'reported_issue': forms.Textarea(attrs={'rows': 3}),
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'internal_notes': forms.Textarea(attrs={'rows': 3}),
            'customer_notes': forms.Textarea(attrs={'rows': 3}),
            'promised_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'approval_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'warranty_expiry': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        organization = kwargs.pop('organization', None)
        branch = kwargs.pop('branch', None)
        super().__init__(*args, **kwargs)
        
        if organization:
            self.fields['customer'].queryset = self.fields['customer'].queryset.filter(
                organization=organization
            )
            self.fields['device'].queryset = self.fields['device'].queryset.filter(
                organization=organization
            )
            self.fields['assigned_to'].queryset = self.fields['assigned_to'].queryset.filter(
                organization=organization
            )
            self.fields['approved_by'].queryset = self.fields['approved_by'].queryset.filter(
                organization=organization
            )


class RepairPartForm(forms.ModelForm):
    """Form for adding parts to a repair order."""
    
    class Meta:
        model = RepairPart
        fields = [
            'part', 'part_name', 'part_code',
            'quantity', 'unit_cost', 'total_cost',
            'serial_number', 'is_warranty', 'notes'
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        organization = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        
        if organization:
            self.fields['part'].queryset = self.fields['part'].queryset.filter(
                organization=organization
            )


class RepairServiceForm(forms.ModelForm):
    """Form for adding services to a repair order."""
    
    class Meta:
        model = RepairService
        fields = [
            'service', 'service_name', 'service_code',
            'quantity', 'unit_price', 'total_price',
            'duration_minutes', 'technician', 'notes'
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        organization = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        
        if organization:
            self.fields['service'].queryset = self.fields['service'].queryset.filter(
                organization=organization
            )
            self.fields['technician'].queryset = self.fields['technician'].queryset.filter(
                organization=organization
            )


class RepairChecklistForm(forms.ModelForm):
    """Form for adding checklist items to a repair order."""
    
    class Meta:
        model = RepairChecklist
        fields = ['item', 'description', 'is_completed', 'sequence']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class RepairAttachmentForm(forms.ModelForm):
    """Form for adding attachments to a repair order."""
    
    class Meta:
        model = RepairAttachment
        fields = ['file', 'file_type', 'title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class RepairTemplateForm(forms.ModelForm):
    """Form for creating and updating repair templates."""
    
    class Meta:
        model = RepairTemplate
        fields = [
            'name', 'code', 'description',
            'repair_type', 'estimated_cost', 'estimated_duration',
            'checklist_items', 'default_parts', 'default_services',
            'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'checklist_items': forms.Textarea(attrs={'rows': 5}),
            'default_parts': forms.Textarea(attrs={'rows': 5}),
            'default_services': forms.Textarea(attrs={'rows': 5}),
        }
    
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


class RepairStatusForm(forms.ModelForm):
    """Form for creating and updating repair statuses."""
    
    class Meta:
        model = RepairStatus
        fields = ['name', 'code', 'description', 'color', 'is_initial', 'is_final', 'sequence']


class RepairPriorityForm(forms.ModelForm):
    """Form for creating and updating repair priorities."""
    
    class Meta:
        model = RepairPriority
        fields = ['name', 'code', 'level', 'color', 'estimated_hours']


class RepairCategoryForm(forms.ModelForm):
    """Form for creating and updating repair categories."""
    
    class Meta:
        model = RepairCategory
        fields = ['name', 'code', 'description', 'parent', 'icon', 'color', 'is_active']


class RepairTypeForm(forms.ModelForm):
    """Form for creating and updating repair types."""
    
    class Meta:
        model = RepairType
        fields = [
            'name', 'code', 'category',
            'description', 'estimated_cost', 'estimated_duration', 'is_active'
        ]


# Quick forms for inline creation
class QuickRepairOrderForm(forms.ModelForm):
    """Simplified form for quick repair order creation."""
    
    class Meta:
        model = RepairOrder
        fields = [
            'customer', 'device', 'device_name',
            'device_imei', 'device_serial',
            'issue_description', 'priority', 'promised_date'
        ]
        widgets = {
            'issue_description': forms.Textarea(attrs={'rows': 3}),
            'promised_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class QuickRepairPartForm(forms.ModelForm):
    """Simplified form for quick part addition."""
    
    class Meta:
        model = RepairPart
        fields = ['part_name', 'quantity', 'unit_cost']


class QuickRepairServiceForm(forms.ModelForm):
    """Simplified form for quick service addition."""
    
    class Meta:
        model = RepairService
        fields = ['service_name', 'quantity', 'unit_price']
