"""
Services for the backups application.
"""
import os
import shutil
import hashlib
from django.conf import settings
from django.utils import timezone
from .models import Backup, BackupSchedule, RestoreLog


class BackupService:
    """
    Service for backup operations.
    """
    
    def __init__(self, request):
        self.request = request
        self.user = request.user
    
    def create_backup(self, description='', backup_type='manual'):
        """
        Create a new database backup.
        """
        try:
            # Create backup directory if it doesn't exist
            backup_dir = os.path.join(settings.BASE_DIR, 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            
            # Generate backup filename
            timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
            file_name = f"backup_{backup_type}_{timestamp}.sqlite3"
            file_path = os.path.join(backup_dir, file_name)
            
            # Get database path
            db_path = settings.DATABASES['default']['NAME']
            
            # Copy database file
            shutil.copy2(db_path, file_path)
            
            # Calculate checksum
            with open(file_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            
            # Get file size
            file_size = os.path.getsize(file_path)
            
            # Create backup record
            backup = Backup.objects.create(
                backup_type=backup_type,
                user=self.user if self.user.is_authenticated else None,
                file_name=file_name,
                file_path=file_path,
                file_size=file_size,
                organization=self.request.current_organization if hasattr(self.request, 'current_organization') else None,
                description=description,
                is_successful=True,
                is_verified=False,
                checksum=file_hash
            )
            
            return self.get_backup_data(backup)
        except Exception as e:
            # Create failed backup record
            Backup.objects.create(
                backup_type=backup_type,
                user=self.user if self.user.is_authenticated else None,
                file_name=f"backup_{backup_type}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.sqlite3",
                file_path='',
                file_size=0,
                organization=self.request.current_organization if hasattr(self.request, 'current_organization') else None,
                description=description,
                is_successful=False,
                error_message=str(e)
            )
            return None
    
    def verify_backup(self, pk):
        """
        Verify a backup file.
        """
        try:
            backup = Backup.objects.get(pk=pk)
            
            # Check if file exists
            if not os.path.exists(backup.file_path):
                backup.is_verified = False
                backup.error_message = 'Backup file not found'
                backup.save()
                return False
            
            # Verify checksum
            with open(backup.file_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            
            if file_hash != backup.checksum:
                backup.is_verified = False
                backup.error_message = 'Checksum mismatch'
                backup.save()
                return False
            
            # Mark as verified
            backup.is_verified = True
            backup.verified_at = timezone.now()
            backup.save()
            
            return True
        except Backup.DoesNotExist:
            return False
    
    def restore_backup(self, pk):
        """
        Restore a backup.
        """
        try:
            backup = Backup.objects.get(pk=pk)
            
            # Verify backup first
            if not self.verify_backup(pk):
                return False
            
            # Get database path
            db_path = settings.DATABASES['default']['NAME']
            
            # Make sure database directory exists
            db_dir = os.path.dirname(db_path)
            os.makedirs(db_dir, exist_ok=True)
            
            # Copy backup file to database location
            shutil.copy2(backup.file_path, db_path)
            
            # Log restore
            RestoreLog.objects.create(
                backup=backup,
                user=self.user if self.user.is_authenticated else None,
                restore_path=db_path,
                is_successful=True,
                started_at=timezone.now(),
                completed_at=timezone.now()
            )
            
            return True
        except Exception as e:
            RestoreLog.objects.create(
                backup=backup,
                user=self.user if self.user.is_authenticated else None,
                restore_path='',
                is_successful=False,
                error_message=str(e),
                started_at=timezone.now(),
                completed_at=timezone.now()
            )
            return False
    
    def delete_backup(self, pk):
        """
        Delete a backup.
        """
        try:
            backup = Backup.objects.get(pk=pk)
            
            # Delete file
            if os.path.exists(backup.file_path):
                os.remove(backup.file_path)
            
            # Delete record
            backup.delete()
            
            return True
        except Backup.DoesNotExist:
            return False
    
    def get_backup_data(self, backup):
        """
        Get backup data for API responses.
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
            'file_path': backup.file_path,
            'file_size': backup.file_size,
            'file_size_display': backup.get_file_size_display(),
            'organization': {
                'id': str(backup.organization.id) if backup.organization else None,
                'name': backup.organization.name if backup.organization else None,
            } if backup.organization else None,
            'description': backup.description,
            'is_successful': backup.is_successful,
            'error_message': backup.error_message,
            'is_verified': backup.is_verified,
            'verified_at': backup.verified_at.isoformat() if backup.verified_at else None,
            'checksum': backup.checksum,
            'created_at': backup.created_at.isoformat(),
        }
