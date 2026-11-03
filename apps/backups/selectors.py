"""
Selectors for the backups application.
"""
from django.db.models import Q
from .models import Backup, BackupSchedule, RestoreLog


class BackupSelector:
    """
    Selector for backup queries.
    """
    
    def __init__(self, request):
        self.request = request
        self.user = request.user
    
    def get_backup(self, pk):
        """
        Get a backup by ID.
        """
        try:
            backup = Backup.objects.get(pk=pk)
            
            # Check access
            if not self.has_backup_access(backup):
                return None
            
            return self.get_backup_data(backup)
        except Backup.DoesNotExist:
            return None
    
    def get_backups(self, **filters):
        """
        Get a list of backups.
        """
        queryset = Backup.objects.all()
        
        # Apply organization filter based on user access
        if self.user.is_authenticated:
            if self.user.is_superuser:
                # Superusers can see all backups
                pass
            else:
                # Regular users can only see backups for their organizations
                from apps.organizations.models import OrganizationMembership
                org_ids = OrganizationMembership.objects.filter(
                    user=self.user
                ).values_list('organization', flat=True)
                queryset = queryset.filter(organization_id__in=org_ids)
        else:
            # Anonymous users can't see any backups
            queryset = queryset.none()
        
        # Apply additional filters
        if 'backup_type' in filters:
            queryset = queryset.filter(backup_type=filters['backup_type'])
        
        if 'is_successful' in filters:
            queryset = queryset.filter(is_successful=filters['is_successful'])
        
        if 'is_verified' in filters:
            queryset = queryset.filter(is_verified=filters['is_verified'])
        
        if 'organization_id' in filters:
            queryset = queryset.filter(organization_id=filters['organization_id'])
        
        if 'start_date' in filters:
            queryset = queryset.filter(created_at__gte=filters['start_date'])
        
        if 'end_date' in filters:
            queryset = queryset.filter(created_at__lte=filters['end_date'])
        
        if 'search' in filters and filters['search']:
            search = filters['search']
            queryset = queryset.filter(
                Q(file_name__icontains=search) |
                Q(description__icontains=search)
            )
        
        return [
            self.get_backup_data(backup) for backup in queryset.order_by('-created_at')[:50]
        ]
    
    def has_backup_access(self, backup):
        """
        Check if user has access to a backup.
        """
        if not self.user.is_authenticated:
            return False
        
        if self.user.is_superuser:
            return True
        
        # Check if backup is for user's organization
        if backup.organization:
            from apps.organizations.models import OrganizationMembership
            return OrganizationMembership.objects.filter(
                organization=backup.organization,
                user=self.user
            ).exists()
        
        # If no organization, check if user created it
        return backup.user == self.user
    
    def get_backup_data(self, backup):
        """
        Get backup data for responses.
        """
        return {
            'id': str(backup.id),
            'backup_type': backup.backup_type,
            'backup_type_display': backup.get_backup_type_display(),
            'user': {
                'id': str(backup.user.id) if backup.user else None,
                'email': backup.user.email if backup.user else None,
                'username': backup.user.username if backup.user else None,
            } if backup.user else None,
            'file_name': backup.file_name,
            'file_size': backup.file_size,
            'file_size_display': backup.get_file_size_display(),
            'organization': {
                'id': str(backup.organization.id) if backup.organization else None,
                'name': backup.organization.name if backup.organization else None,
            } if backup.organization else None,
            'description': backup.description,
            'is_successful': backup.is_successful,
            'is_verified': backup.is_verified,
            'created_at': backup.created_at,
        }
    
    def get_backup_schedules(self, **filters):
        """
        Get a list of backup schedules.
        """
        queryset = BackupSchedule.objects.all()
        
        # Apply organization filter based on user access
        if self.user.is_authenticated:
            if self.user.is_superuser:
                # Superusers can see all schedules
                pass
            else:
                # Regular users can only see schedules for their organizations
                from apps.organizations.models import OrganizationMembership
                org_ids = OrganizationMembership.objects.filter(
                    user=self.user
                ).values_list('organization', flat=True)
                queryset = queryset.filter(organization_id__in=org_ids)
        else:
            # Anonymous users can't see any schedules
            queryset = queryset.none()
        
        # Apply additional filters
        if 'is_active' in filters:
            queryset = queryset.filter(is_active=filters['is_active'])
        
        if 'organization_id' in filters:
            queryset = queryset.filter(organization_id=filters['organization_id'])
        
        return [
            self.get_backup_schedule_data(schedule) for schedule in queryset.order_by('name')
        ]
    
    def get_backup_schedule_data(self, schedule):
        """
        Get backup schedule data for responses.
        """
        return {
            'id': str(schedule.id),
            'name': schedule.name,
            'frequency': schedule.frequency,
            'frequency_display': schedule.get_frequency_display(),
            'day_of_week': schedule.day_of_week,
            'day_of_month': schedule.day_of_month,
            'time': schedule.time,
            'organization': {
                'id': str(schedule.organization.id) if schedule.organization else None,
                'name': schedule.organization.name if schedule.organization else None,
            } if schedule.organization else None,
            'max_backups': schedule.max_backups,
            'backup_directory': schedule.backup_directory,
            'is_active': schedule.is_active,
            'last_run': schedule.last_run.isoformat() if schedule.last_run else None,
            'last_run_successful': schedule.last_run_successful,
            'created_at': schedule.created_at,
            'updated_at': schedule.updated_at,
        }
