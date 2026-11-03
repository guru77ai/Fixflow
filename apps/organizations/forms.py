"""
Forms for the organizations application.
"""
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Organization, OrganizationMembership


class OrganizationForm(forms.ModelForm):
    """
    Form for creating and editing organizations.
    """
    name = forms.CharField(
        label=_('Name'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Organization Name'),
        })
    )
    legal_name = forms.CharField(
        label=_('Legal Name'),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Legal Name'),
        })
    )
    code = forms.CharField(
        label=_('Code'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Organization Code'),
        })
    )
    logo = forms.ImageField(
        label=_('Logo'),
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
        })
    )
    tax_identification_number = forms.CharField(
        label=_('Tax Identification Number'),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Tax ID'),
        })
    )
    tax_authority = forms.CharField(
        label=_('Tax Authority'),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Tax Authority'),
        })
    )
    business_activity = forms.CharField(
        label=_('Business Activity'),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Business Activity'),
        })
    )
    industry = forms.ChoiceField(
        label=_('Industry'),
        choices=Organization.INDUSTRY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
    currency = forms.CharField(
        label=_('Currency'),
        initial='DZD',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Currency'),
        })
    )
    default_language = forms.ChoiceField(
        label=_('Default Language'),
        choices=Organization.LANGUAGE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
    timezone = forms.CharField(
        label=_('Timezone'),
        initial='Africa/Algiers',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Timezone'),
        })
    )
    address = forms.CharField(
        label=_('Address'),
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': _('Address'),
            'rows': 2,
        })
    )
    city = forms.CharField(
        label=_('City'),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('City'),
        })
    )
    state = forms.CharField(
        label=_('State'),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('State'),
        })
    )
    postal_code = forms.CharField(
        label=_('Postal Code'),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Postal Code'),
        })
    )
    country = forms.CharField(
        label=_('Country'),
        initial='Algeria',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Country'),
        })
    )
    phone = forms.CharField(
        label=_('Phone'),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Phone'),
        })
    )
    secondary_phone = forms.CharField(
        label=_('Secondary Phone'),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Secondary Phone'),
        })
    )
    email = forms.EmailField(
        label=_('Email'),
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Email'),
        })
    )
    website = forms.URLField(
        label=_('Website'),
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': _('Website'),
        })
    )
    invoice_prefix = forms.CharField(
        label=_('Invoice Prefix'),
        initial='INV',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Invoice Prefix'),
        })
    )
    repair_prefix = forms.CharField(
        label=_('Repair Prefix'),
        initial='REP',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Repair Prefix'),
        })
    )
    accounting_method = forms.ChoiceField(
        label=_('Accounting Method'),
        choices=Organization.ACCOUNTING_METHOD_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
    fiscal_year_start = forms.ChoiceField(
        label=_('Fiscal Year Start'),
        choices=Organization.FISCAL_YEAR_START_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
    notes = forms.CharField(
        label=_('Notes'),
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': _('Notes'),
            'rows': 3,
        })
    )
    is_active = forms.BooleanField(
        label=_('Active'),
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )
    
    class Meta:
        model = Organization
        fields = [
            'name', 'legal_name', 'code', 'logo',
            'tax_identification_number', 'tax_authority',
            'business_activity', 'industry',
            'currency', 'default_language', 'timezone',
            'address', 'city', 'state', 'postal_code', 'country',
            'phone', 'secondary_phone', 'email', 'website',
            'invoice_prefix', 'repair_prefix',
            'accounting_method', 'fiscal_year_start',
            'notes', 'is_active'
        ]


class OrganizationMembershipForm(forms.ModelForm):
    """
    Form for managing organization memberships.
    """
    user = forms.CharField(
        label=_('User'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('User Email or Username'),
        })
    )
    is_owner = forms.BooleanField(
        label=_('Owner'),
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )
    is_admin = forms.BooleanField(
        label=_('Administrator'),
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )
    can_manage_users = forms.BooleanField(
        label=_('Can Manage Users'),
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )
    can_manage_settings = forms.BooleanField(
        label=_('Can Manage Settings'),
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )
    can_access_all_branches = forms.BooleanField(
        label=_('Can Access All Branches'),
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )
    
    class Meta:
        model = OrganizationMembership
        fields = [
            'user', 'is_owner', 'is_admin',
            'can_manage_users', 'can_manage_settings',
            'can_access_all_branches'
        ]
