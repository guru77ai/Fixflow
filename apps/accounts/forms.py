"""
Forms for the accounts application.
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import User


class UserLoginForm(AuthenticationForm):
    """
    Custom login form.
    """
    username = forms.CharField(
        label=_('Username or Email'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Username or Email'),
            'autofocus': True,
        })
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Password'),
        })
    )
    remember_me = forms.BooleanField(
        label=_('Remember me'),
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('remember_me', None)
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and '@' in username:
            # If username contains @, treat it as email
            try:
                user = User.objects.get(email=username)
                return user.username
            except User.DoesNotExist:
                return username
        return username


class UserRegistrationForm(UserCreationForm):
    """
    Custom user registration form.
    """
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Email'),
        })
    )
    username = forms.CharField(
        label=_('Username'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Username'),
        })
    )
    first_name = forms.CharField(
        label=_('First Name'),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('First Name'),
        })
    )
    last_name = forms.CharField(
        label=_('Last Name'),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Last Name'),
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
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Password'),
        })
    )
    password2 = forms.CharField(
        label=_('Confirm Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Confirm Password'),
        })
    )
    
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'phone', 'password1', 'password2')


class UserProfileForm(forms.ModelForm):
    """
    User profile form.
    """
    avatar = forms.ImageField(
        label=_('Avatar'),
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
        })
    )
    first_name = forms.CharField(
        label=_('First Name'),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('First Name'),
        })
    )
    last_name = forms.CharField(
        label=_('Last Name'),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Last Name'),
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
    date_of_birth = forms.DateField(
        label=_('Date of Birth'),
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        })
    )
    gender = forms.ChoiceField(
        label=_('Gender'),
        required=False,
        choices=[
            ('', _('Select Gender')),
            ('male', _('Male')),
            ('female', _('Female')),
            ('other', _('Other')),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
    language = forms.ChoiceField(
        label=_('Language'),
        choices=[
            ('fr', _('Français')),
            ('ar', _('العربية')),
            ('en', _('English')),
        ],
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
    
    class Meta:
        model = User
        fields = (
            'avatar', 'first_name', 'last_name', 'phone', 
            'date_of_birth', 'gender', 'language', 'timezone'
        )


class UserSettingsForm(forms.ModelForm):
    """
    User settings form.
    """
    theme = forms.ChoiceField(
        label=_('Theme'),
        choices=[
            ('system', _('System')),
            ('light', _('Light')),
            ('dark', _('Dark')),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
    
    class Meta:
        model = User
        fields = ('theme',)


class PasswordChangeForm(forms.Form):
    """
    Password change form.
    """
    current_password = forms.CharField(
        label=_('Current Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Current Password'),
        })
    )
    new_password1 = forms.CharField(
        label=_('New Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('New Password'),
        })
    )
    new_password2 = forms.CharField(
        label=_('Confirm New Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Confirm New Password'),
        })
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise forms.ValidationError(_('Your current password is incorrect.'))
        return current_password
    
    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError(_('The new passwords do not match.'))
        return new_password2
