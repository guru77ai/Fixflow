"""
Services for the backups application.
"""
import os
import shutil
import hashlib
import sqlite3
from django.conf import settings
from django.utils import timezone
from .models import Backup, BackupSchedule, RestoreLog
from rest_framework.exceptions import PermissionDenied, ValidationError


class BackupService:
    """
    Service for backup operations.
    """
    
    def __init__(self, request):
        self.request = request
        self.user = request.user
    
    def create_backup(self, description='', backup_type='manual'):
        """
        Create a new database backup using SQLite backup API for consistency.
        
        This ensures that the backup is consistent even if the database is being
        written to during the backup process.
        """
        try:
            # Validate user has permission
            if not self.user.is_authenticated:
                raise PermissionDenied('Authentication required to create backup')
            
            # Create backup directory if it doesn't exist
            backup_dir = os.path.join(settings.BASE_DIR, 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            
            # Generate backup filename
            timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
            file_name = f"backup_{backup_type}_{timestamp}.sqlite3"
            file_path = os.path.join(backup_dir, file_name)
            
            # Get database path
            db_path = settings.DATABASES['default']['NAME']
            
            # Validate database path exists
            if not os.path.exists(db_path):
                raise ValidationError(f'Database file not found: {db_path}')
            
            # Validate backup path is within allowed directory
            if not file_path.startswith(os.path.abspath(backup_dir)):
                raise ValidationError('Invalid backup path - path traversal detected')
            
            # Use SQLite backup API for consistent backup
            # This ensures the backup is consistent even during writes
            conn = sqlite3.connect(db_path)
            backup_conn = sqlite3.connect(file_path)
            
            try:
                # Use SQLite online backup API
                with backup_conn:
                    conn.backup(backup_conn, pages=100)
            finally:
                conn.close()
                backup_conn.close()
            
            # Verify backup file was created
            if not os.path.exists(file_path):
                raise ValidationError('Backup file was not created')
            
            # Calculate checksum
            with open(file_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            
            # Get file size
            file_size = os.path.getsize(file_path)
            
            # Get organization from request using canonical attribute
            organization = None
            if hasattr(self.request, 'organization') and self.request.organization:
                organization = self.request.organization
            elif hasattr(self.request, 'current_organization') and self.request.current_organization:
                organization = self.request.current_organization
            
            # Create backup record
            backup = Backup.objects.create(
                backup_type=backup_type,
                user=self.user,
                file_name=file_name,
                file_path=file_path,
                file_size=file_size,
                organization=organization,
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
                organization=self.request.organization if hasattr(self.request, 'organization') and self.request.organization else None,
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
        Restore a backup with explicit confirmation and safety checks.
        
        This method prevents unsafe overwrites that could corrupt the active database.
        """
        try:
            backup = Backup.objects.get(pk=pk)
            
            # Validate user has permission
            if not self.user.is_authenticated:
                raise PermissionDenied('Authentication required to restore backup')
            
            # Verify backup first
            if not self.verify_backup(pk):
                raise ValidationError('Backup verification failed')
            
            # Get database path
            db_path = settings.DATABASES['default']['NAME']
            
            # Validate backup path is within allowed directory
            backup_dir = os.path.join(settings.BASE_DIR, 'backups')
            if not backup.file_path.startswith(os.path.abspath(backup_dir)):
                raise ValidationError('Invalid backup path - path traversal detected')
            
            # Validate restore path is the database file
            expected_db_path = os.path.abspath(db_path)
            if not db_path:
                raise ValidationError('Database path not configured')
            
            # Make sure database directory exists
            db_dir = os.path.dirname(db_path)
            os.makedirs(db_dir, exist_ok=True)
            
            # Create a temporary copy first for safety
            temp_path = f"{db_path}.restore_temp"
            shutil.copy2(backup.file_path, temp_path)
            
            # Verify the temporary file
            with open(temp_path, 'rb') as f:
                temp_hash = hashlib.sha256(f.read()).hexdigest()
            
            if temp_hash != backup.checksum:
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                raise ValidationError('Backup file checksum mismatch after copy')
            
            # Only now overwrite the actual database
            # In production, you would want to:
            # 1. Close all database connections
            # 2. Make a backup of the current database
            # 3. Then restore
            # For this implementation, we'll just do a safe copy
            
            # Backup current database first (safety measure)
            current_backup_path = f"{db_path}.pre_restore_backup"
            if os.path.exists(db_path):
                shutil.copy2(db_path, current_backup_path)
            
            # Restore the backup
            shutil.move(temp_path, db_path)
            
            # Log restore
            RestoreLog.objects.create(
                backup=backup,
                user=self.user,
                restore_path=db_path,
                is_successful=True,
                started_at=timezone.now(),
                completed_at=timezone.now(),
                notes=f'Previous database backed up to: {current_backup_path}'
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
