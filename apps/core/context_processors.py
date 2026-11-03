"""
Context processors for the core application.
"""
from django.conf import settings
from django.utils import timezone
from apps.organizations.models import Organization, OrganizationMembership
from apps.branches.models import Branch, BranchUserAccess
from apps.notifications.models import Notification


def organization_context(request):
    """
    Add organization context to all templates.
    """
    context = {
        'current_organization': None,
        'organizations': [],
    }
    
    if request.user.is_authenticated:
        # Get user's organizations through memberships
        memberships = OrganizationMembership.objects.filter(
            user=request.user
        ).select_related('organization').order_by('organization__name')
        
        context['organizations'] = [m.organization for m in memberships]
        
        # Set current organization
        if 'organization_id' in request.session:
            org_id = request.session['organization_id']
            for org in context['organizations']:
                if str(org.id) == str(org_id):
                    context['current_organization'] = org
                    break
        
        # Fallback to first organization
        if not context['current_organization'] and context['organizations']:
            context['current_organization'] = context['organizations'][0]
            request.session['organization_id'] = str(context['current_organization'].id)
    
    return context


def branch_context(request):
    """
    Add branch context to all templates.
    """
    context = {
        'current_branch': None,
        'branches': [],
    }
    
    if request.user.is_authenticated:
        # Get current organization
        current_org = None
        if 'organization_id' in request.session:
            try:
                current_org = Organization.objects.get(id=request.session['organization_id'])
            except Organization.DoesNotExist:
                pass
        
        if current_org:
            # Get branches for current organization
            branches = Branch.objects.filter(
                organization=current_org,
                is_active=True
            ).select_related('manager').order_by('code')
            
            context['branches'] = list(branches)
            
            # Set current branch
            if 'branch_id' in request.session:
                branch_id = request.session['branch_id']
                for branch in context['branches']:
                    if str(branch.id) == str(branch_id):
                        context['current_branch'] = branch
                        break
            
            # Fallback to first branch or user's branch
            if not context['current_branch']:
                if context['branches']:
                    context['current_branch'] = context['branches'][0]
                    request.session['branch_id'] = str(context['current_branch'].id)
                elif request.user.branch:
                    context['current_branch'] = request.user.branch
                    request.session['branch_id'] = str(context['current_branch'].id)
    
    return context


def settings_context(request):
    """
    Add application settings context to all templates.
    """
    from apps.settings.models import SystemSetting
    
    context = {
        'app_settings': {},
        'current_year': timezone.now().year,
        'default_currency': settings.DEFAULT_CURRENCY,
    }
    
    # Load system settings
    try:
        settings_list = SystemSetting.objects.all()
        for setting in settings_list:
            context['app_settings'][setting.key] = setting.get_value()
    except Exception:
        pass
    
    return context


def notifications_context(request):
    """
    Add notifications context to all templates.
    """
    context = {
        'unread_notifications': 0,
        'recent_notifications': [],
    }
    
    if request.user.is_authenticated:
        # Count unread notifications
        context['unread_notifications'] = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
        
        # Get recent notifications
        context['recent_notifications'] = Notification.objects.filter(
            user=request.user
        ).order_by('-created_at')[:5]
    
    return context


def user_context(request):
    """
    Add user context to all templates.
    """
    context = {
        'user_roles': [],
        'user_permissions': [],
    }
    
    if request.user.is_authenticated:
        context['user_roles'] = [role.name for role in request.user.roles.all()]
        context['user_permissions'] = list(request.user.get_permissions())
    
    return context
