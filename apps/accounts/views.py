"""
Views for the accounts application.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm, UserSettingsForm
from .services import AccountService
from .selectors import AccountSelector


def login_view(request):
    """
    User login view.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    form = UserLoginForm()
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, _('You have successfully logged in.'))
                
                # Redirect to next URL or dashboard
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                messages.error(request, _('Invalid username or password.'))
        else:
            messages.error(request, _('Please correct the errors below.'))
    
    context = {
        'page_title': _('Login'),
        'form': form,
    }
    
    return render(request, 'accounts/login.html', context)


from django.views.decorators.http import require_POST

@require_POST
def logout_view(request):
    """
    User logout view.
    Requires POST to prevent CSRF attacks.
    """
    logout(request)
    messages.success(request, _('You have been logged out.'))
    return redirect('accounts:login')


def register_view(request):
    """
    User registration view.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    form = UserRegistrationForm()
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, _('Your account has been created. Please log in.'))
            return redirect('accounts:login')
        else:
            messages.error(request, _('Please correct the errors below.'))
    
    context = {
        'page_title': _('Register'),
        'form': form,
    }
    
    return render(request, 'accounts/register.html', context)


def password_reset_view(request):
    """
    Password reset request view.
    """
    form = PasswordResetForm()
    
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                email_template_name='accounts/email/password_reset_email.html',
                subject_template_name='accounts/email/password_reset_subject.txt',
            )
            messages.success(request, _('Password reset email has been sent.'))
            return redirect('password_reset_done')
    
    context = {
        'page_title': _('Password Reset'),
        'form': form,
    }
    
    return render(request, 'accounts/password_reset.html', context)


def password_reset_done_view(request):
    """
    Password reset done view.
    """
    context = {
        'page_title': _('Password Reset Sent'),
    }
    
    return render(request, 'accounts/password_reset_done.html', context)


def password_reset_confirm_view(request, uidb64, token):
    """
    Password reset confirm view.
    Validates the token and allows user to set a new password.
    """
    from django.contrib.auth.tokens import default_token_generator
    from django.contrib.auth import get_user_model
    from django.utils.http import urlsafe_base64_decode
    
    User = get_user_model()
    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            from django.contrib.auth.forms import SetPasswordForm
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, _('Your password has been reset. Please log in.'))
                return redirect('accounts:login')
        else:
            form = SetPasswordForm(user)
        
        context = {
            'page_title': _('Reset Password'),
            'form': form,
            'uidb64': uidb64,
            'token': token,
        }
        return render(request, 'accounts/password_reset_confirm.html', context)
    else:
        messages.error(request, _('The reset link is no longer valid.'))
        return redirect('accounts:password_reset')


@login_required
def password_change_view(request):
    from django.contrib.auth.forms import PasswordChangeForm
    from django.contrib.auth import update_session_auth_hash
    
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, _('Your password has been changed successfully.'))
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(user=request.user)
    
    context = {
        'page_title': _('Change Password'),
        'form': form,
    }
    return render(request, 'accounts/password_change.html', context)


def password_reset_complete_view(request):
    """
    Password reset complete view.
    """
    context = {
        'page_title': _('Password Reset Complete'),
    }
    
    return render(request, 'accounts/password_reset_complete.html', context)


@login_required
def profile_view(request):
    """
    User profile view.
    """
    selector = AccountSelector(request)
    user_data = selector.get_user_profile()
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your profile has been updated.'))
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'page_title': _('Profile'),
        'form': form,
        'user_data': user_data,
    }
    
    return render(request, 'accounts/profile.html', context)


@login_required
def settings_view(request):
    """
    User settings view.
    """
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your settings have been updated.'))
            return redirect('settings')
    else:
        form = UserSettingsForm(instance=request.user)
    
    context = {
        'page_title': _('Settings'),
        'form': form,
    }
    
    return render(request, 'accounts/settings.html', context)


@login_required
def users_view(request):
    """
    User management view.
    Requires organization context and user management permissions.
    """
    from apps.organizations.models import OrganizationMembership
    
    # Verify organization context
    if not hasattr(request, 'organization') or not request.organization:
        from django.contrib import messages
        messages.error(request, _("Organization context required"))
        return redirect('dashboard')
    
    # Verify user has permission to view users in this organization
    has_permission = OrganizationMembership.objects.filter(
        user=request.user,
        organization=request.organization,
        is_active=True,
        can_manage_users=True
    ).exists()
    
    if not has_permission and not request.user.is_superuser:
        from django.contrib import messages
        messages.error(request, _("You do not have permission to view users"))
        return redirect('dashboard')
    
    selector = AccountSelector(request)
    users = selector.get_users()
    
    context = {
        'page_title': _('User Management'),
        'users': users,
    }
    
    return render(request, 'accounts/users.html', context)


# API Views

class UserAPIView(APIView):
    """
    API endpoint for user operations.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        selector = AccountSelector(request)
        user_data = selector.get_user_data(request.user)
        return Response(user_data)


class UserListAPIView(APIView):
    """
    API endpoint for listing users.
    Only returns users from the current organization.
    Requires organization admin or user management permissions.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        from rest_framework.exceptions import PermissionDenied
        from apps.organizations.models import OrganizationMembership
        
        # Verify organization context
        if not hasattr(request, 'organization') or not request.organization:
            raise PermissionDenied("Organization context required")
        
        # Verify user has permission to view users in this organization
        has_permission = OrganizationMembership.objects.filter(
            user=request.user,
            organization=request.organization,
            is_active=True,
            can_manage_users=True
        ).exists()
        
        if not has_permission:
            # Also check if user is superuser
            if not request.user.is_superuser:
                raise PermissionDenied("You do not have permission to view users in this organization")
        
        selector = AccountSelector(request)
        users = selector.get_users()
        return Response(users)
