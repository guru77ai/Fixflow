"""
Selectors for the accounts application.
"""
from django.db.models import Q
from .models import User, Role, Permission, UserSession, LoginHistory


class AccountSelector:
    """
    Selector for account-related queries.
    """
    
    def __init__(self, request):
        self.request = request
        self.user = request.user
    
    def get_user(self, user_id):
        """
        Get a user by ID.
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    
    def get_user_by_email(self, email):
        """
        Get a user by email.
        """
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
    
    def get_user_by_username(self, username):
        """
        Get a user by username.
        """
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None
    
    def get_users(self, **filters):
        """
        Get a list of users.
        """
        queryset = User.objects.all()
        
        # Apply organization filter
        if hasattr(self.request, 'current_organization') and self.request.current_organization:
            queryset = queryset.filter(
                organization=self.request.current_organization
            )
        
        # Apply filters
        if 'is_active' in filters:
            queryset = queryset.filter(is_active=filters['is_active'])
        
        if 'search' in filters and filters['search']:
            search = filters['search']
            queryset = queryset.filter(
                Q(email__icontains=search) |
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        
        return [
            {
                'id': str(user.id),
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': user.phone,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
                'last_login': user.last_login.isoformat() if user.last_login else None,
                'date_joined': user.created_at.isoformat(),
                'roles': [role.name for role in user.roles.all()],
            }
            for user in queryset.order_by('-created_at')
        ]
    
    def get_roles(self, **filters):
        """
        Get a list of roles.
        """
        queryset = Role.objects.all()
        
        if 'is_active' in filters:
            queryset = queryset.filter(is_active=filters['is_active'])
        
        if 'search' in filters and filters['search']:
            search = filters['search']
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search)
            )
        
        return [
            {
                'id': str(role.id),
                'name': role.name,
                'code': role.code,
                'description': role.description,
                'is_system': role.is_system,
                'level': role.level,
                'is_active': role.is_active,
                'created_at': role.created_at.isoformat(),
            }
            for role in queryset.order_by('level', 'name')
        ]
    
    def get_permissions(self, **filters):
        """
        Get a list of permissions.
        """
        queryset = Permission.objects.all()
        
        if 'model' in filters:
            queryset = queryset.filter(model=filters['model'])
        
        if 'action' in filters:
            queryset = queryset.filter(action=filters['action'])
        
        return [
            {
                'id': str(perm.id),
                'name': perm.name,
                'codename': perm.codename,
                'model': perm.model,
                'action': perm.action,
                'description': perm.description,
            }
            for perm in queryset.order_by('model', 'action', 'name')
        ]
    
    def get_user_profile(self):
        """
        Get the current user's profile data.
        """
        user = self.user
        if not user.is_authenticated:
            return None
        
        return {
            'id': str(user.id),
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
            'avatar': user.avatar.url if user.avatar else None,
            'date_of_birth': user.date_of_birth.isoformat() if user.date_of_birth else None,
            'gender': user.gender,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'language': user.language,
            'timezone': user.timezone,
            'theme': user.theme,
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'date_joined': user.created_at.isoformat(),
            'roles': [
                {
                    'id': str(role.id),
                    'name': role.name,
                    'code': role.code,
                }
                for role in user.roles.all()
            ],
            'permissions': list(user.get_permissions()),
            'login_count': user.login_count,
        }
    
    def get_user_data(self, user):
        """
        Get user data for API responses.
        """
        return {
            'id': str(user.id),
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
            'avatar': user.avatar.url if user.avatar else None,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'date_joined': user.created_at.isoformat(),
            'roles': [role.name for role in user.roles.all()],
        }
    
    def get_sessions(self, user):
        """
        Get user sessions.
        """
        sessions = UserSession.objects.filter(user=user).order_by('-created_at')
        
        return [
            {
                'id': str(session.id),
                'session_key': session.session_key,
                'ip_address': session.ip_address,
                'user_agent': session.user_agent,
                'is_active': session.is_active,
                'created_at': session.created_at.isoformat(),
                'expired_at': session.expired_at.isoformat() if session.expired_at else None,
            }
            for session in sessions
        ]
    
    def get_login_history(self, user):
        """
        Get user login history.
        """
        history = LoginHistory.objects.filter(user=user).order_by('-login_time')
        
        return [
            {
                'id': str(item.id),
                'ip_address': item.ip_address,
                'user_agent': item.user_agent,
                'login_time': item.login_time.isoformat(),
                'logout_time': item.logout_time.isoformat() if item.logout_time else None,
                'is_successful': item.is_successful,
                'failure_reason': item.failure_reason,
            }
            for item in history
        ]
