"""
Forms for the branches application.
"""
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Branch
from apps.organizations.models import Organization


class BranchForm(forms.ModelForm):
    """
    Form for creating and editing branches.
    """
    organization = forms.ModelChoiceField(
        label=_('Organization'),
        queryset=None,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
    code = forms.CharField(
        label=_('Branch Code'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Branch Code'),
        })
    )
    name = forms.CharField(
        label=_('Name'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Branch Name'),
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
    manager = forms.ModelChoiceField(
        label=_('Branch Manager'),
        queryset=None,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
    is_main_branch = forms.BooleanField(
        label=_('Main Branch'),
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )
    auto_generate_documents = forms.BooleanField(
        label=_('Auto Generate Documents'),
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
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
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        
        # Set organization queryset based on user access
        if user and user.is_authenticated:
            from apps.organizations.models import OrganizationMembership
            if user.is_superuser:
                org_queryset = Organization.objects.all()
            else:
                memberships = OrganizationMembership.objects.filter(user=user)
                org_queryset = Organization.objects.filter(id__in=[m.organization_id for m in memberships])
            
            self.fields['organization'].queryset = org_queryset
            
            # Set manager queryset based on organization
            if 'organization' in self.data:
                org_id = self.data['organization']
                from django.contrib.auth import get_user_model
                User = get_user_model()
                self.fields['manager'].queryset = User.objects.filter(
                    organization_id=org_id
                )
            elif self.instance and self.instance.organization:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                self.fields['manager'].queryset = User.objects.filter(
                    organization=self.instance.organization
                )
            else:
                self.fields['manager'].queryset = User.objects.none()
        else:
            self.fields['organization'].queryset = Organization.objects.none()
            self.fields['manager'].queryset = User.objects.none()
    
    class Meta:
        model = Branch
        fields = [
            'organization', 'code', 'name',
            'address', 'city', 'state', 'postal_code', 'country',
            'phone', 'secondary_phone', 'email', 'website',
            'manager', 'is_main_branch', 'auto_generate_documents',
            'notes', 'is_active'
        ]
    
    def save(self, commit=True):
        branch = super().save(commit=False)
        
        # Set organization if not set
        if not branch.organization and self.user:
            from apps.organizations.models import OrganizationMembership
            membership = OrganizationMembership.objects.filter(
                user=self.user
            ).first()
            if membership:
                branch.organization = membership.organization
        
        if commit:
            branch.save()
        
        return branch
