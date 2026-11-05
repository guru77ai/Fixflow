"""
Forms for POS module
"""
from django import forms
from .models import Sale, CashRegister, PaymentMethod, POSSettings


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = [
            'sale_type', 'status', 'customer', 'cash_register',
            'subtotal', 'discount', 'tax_amount', 'total_amount',
            'amount_paid', 'balance', 'payment_method',
            'payment_reference', 'payment_status',
            'is_credit', 'credit_days', 'due_date',
            'is_invoice', 'invoice_number', 'sold_by', 'notes'
        ]
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        organization = kwargs.pop('organization', None)
        branch = kwargs.pop('branch', None)
        super().__init__(*args, **kwargs)
        
        if organization:
            self.fields['customer'].queryset = self.fields['customer'].queryset.filter(organization=organization)
            self.fields['cash_register'].queryset = self.fields['cash_register'].queryset.filter(organization=organization)
            self.fields['sold_by'].queryset = self.fields['sold_by'].queryset.filter(organization=organization)


class CashRegisterForm(forms.ModelForm):
    class Meta:
        model = CashRegister
        fields = ['name', 'code', 'initial_amount', 'is_active']
    
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


class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['name', 'code', 'description', 'is_active', 'is_cash', 'is_card', 'is_mobile', 'is_online', 'icon']


class POSSettingsForm(forms.ModelForm):
    class Meta:
        model = POSSettings
        fields = [
            'receipt_header', 'receipt_footer',
            'default_payment_method', 'default_cash_register',
            'show_customer_display', 'auto_print_receipt', 'auto_email_receipt',
            'tax_included', 'default_tax_rate',
            'allow_credit_sales', 'credit_limit'
        ]
        widgets = {
            'receipt_header': forms.Textarea(attrs={'rows': 3}),
            'receipt_footer': forms.Textarea(attrs={'rows': 3}),
        }


class QuickSaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer', 'cash_register', 'notes']
