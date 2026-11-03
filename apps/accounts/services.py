"""
Services for the accounts application.
"""
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import User, Role, Permission, UserSession, LoginHistory


class AccountService:
    """
    Service for account-related operations.
    """
    
    @staticmethod
    def create_user(email, username, password=None, **extra_fields):
        """
        Create a new user.
        """
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
            **extra_fields
        )
        return user
    
    @staticmethod
    def create_superuser(email, username, password=None, **extra_fields):
        """
        Create a new superuser.
        """
        user = User.objects.create_superuser(
            email=email,
            username=username,
            password=password,
            **extra_fields
        )
        return user
    
    @staticmethod
    def authenticate_user(request, username, password):
        """
        Authenticate a user.
        """
        return authenticate(request, username=username, password=password)
    
    @staticmethod
    def create_role(name, code, **extra_fields):
        """
        Create a new role.
        """
        role = Role.objects.create(
            name=name,
            code=code,
            **extra_fields
        )
        return role
    
    @staticmethod
    def create_permission(name, codename, **extra_fields):
        """
        Create a new permission.
        """
        permission = Permission.objects.create(
            name=name,
            codename=codename,
            **extra_fields
        )
        return permission
    
    @staticmethod
    def assign_role_to_user(user, role):
        """
        Assign a role to a user.
        """
        user.roles.add(role)
        return user
    
    @staticmethod
    def remove_role_from_user(user, role):
        """
        Remove a role from a user.
        """
        user.roles.remove(role)
        return user
    
    @staticmethod
    def assign_permission_to_role(role, permission):
        """
        Assign a permission to a role.
        """
        role.permissions.add(permission)
        return role
    
    @staticmethod
    def remove_permission_from_role(role, permission):
        """
        Remove a permission from a role.
        """
        role.permissions.remove(permission)
        return role
    
    @staticmethod
    def create_session(user, request):
        """
        Create a user session.
        """
        session_key = request.session.session_key
        if session_key:
            session = UserSession.objects.create(
                user=user,
                session_key=session_key,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
            )
            return session
        return None
    
    @staticmethod
    def end_session(session_key):
        """
        End a user session.
        """
        UserSession.objects.filter(session_key=session_key).update(
            is_active=False,
            expired_at=timezone.now()
        )
    
    @staticmethod
    def log_login(user, request, success=True, error_message=None):
        """
        Log a user login attempt.
        """
        history = LoginHistory.objects.create(
            user=user,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            login_time=timezone.now(),
            is_successful=success,
            failure_reason=error_message
        )
        return history
    
    @staticmethod
    def log_logout(user, request):
        """
        Log a user logout.
        """
        LoginHistory.objects.filter(
            user=user,
            logout_time__isnull=True
        ).update(
            logout_time=timezone.now()
        )
