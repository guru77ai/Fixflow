"""
Views for the backups application.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse, FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Backup, BackupSchedule, RestoreLog
from .services import BackupService
from .selectors import BackupSelector
import os
from django.conf import settings


# Frontend Views

@login_required
def backup_list_view(request):
    """
    List all backups.
    """
    selector = BackupSelector(request)
    backups = selector.get_backups()
    
    context = {
        'page_title': _('Backups'),
        'backups': backups,
    }
    
    return render(request, 'backups/list.html', context)


@login_required
def backup_create_view(request):
    """
    Create a new backup.
    """
    if request.method == 'POST':
        service = BackupService(request)
        backup = service.create_backup(
            description=request.POST.get('description', ''),
            backup_type='manual'
        )
        
        if backup:
            messages.success(request, _('Backup created successfully.'))
            return redirect('backups:list')
        else:
            messages.error(request, _('Failed to create backup.'))
    
    context = {
        'page_title': _('Create Backup'),
    }
    
    return render(request, 'backups/create.html', context)


@login_required
def backup_download_view(request, pk):
    """
    Download a backup file.
    """
    backup = get_object_or_404(Backup, pk=pk)
    
    # Check access
    selector = BackupSelector(request)
    if not selector.has_backup_access(backup):
        messages.error(request, _('You do not have access to this backup.'))
        return redirect('backups:list')
    
    # Serve the file
    file_path = backup.file_path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{backup.file_name}"'
            return response
    
    messages.error(request, _('Backup file not found.'))
    return redirect('backups:list')


@login_required
def backup_delete_view(request, pk):
    """
    Delete a backup.
    """
    backup = get_object_or_404(Backup, pk=pk)
    
    # Check access
    selector = BackupSelector(request)
    if not selector.has_backup_access(backup):
        messages.error(request, _('You do not have access to this backup.'))
        return redirect('backups:list')
    
    if request.method == 'POST':
        # Soft delete
        backup.is_active = False
        backup.save()
        messages.success(request, _('Backup deleted successfully.'))
        return redirect('backups:list')
    
    context = {
        'page_title': _('Delete Backup'),
        'backup': backup,
    }
    
    return render(request, 'backups/delete.html', context)


# API Views

class BackupListAPIView(APIView):
    """
    API endpoint for listing backups.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        selector = BackupSelector(request)
        backups = selector.get_backups()
        return Response(backups)
    
    def post(self, request):
        service = BackupService(request)
        backup = service.create_backup(
            description=request.data.get('description', ''),
            backup_type=request.data.get('backup_type', 'manual')
        )
        if backup:
            return Response(backup, status=status.HTTP_201_CREATED)
        return Response(
            {'error': 'Failed to create backup'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class BackupDetailAPIView(APIView):
    """
    API endpoint for backup details.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        selector = BackupSelector(request)
        backup = selector.get_backup(pk)
        if backup:
            return Response(backup)
        return Response({'error': 'Backup not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        service = BackupService(request)
        success = service.delete_backup(pk)
        if success:
            return Response({'message': 'Backup deleted successfully'})
        return Response({'error': 'Backup not found'}, status=status.HTTP_404_NOT_FOUND)
