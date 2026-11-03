"""
Views for the settings application.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import SystemSetting, OrganizationSetting, BranchSetting, UserSetting
from .services import SettingsService
from .selectors import SettingsSelector


# Frontend Views

@login_required
def general_settings_view(request):
    """
    General settings view.
    """
    selector = SettingsSelector(request)
    settings = selector.get_system_settings()
    
    context = {
        'page_title': _('General Settings'),
        'settings': settings,
    }
    
    return render(request, 'settings/general.html', context)


# API Views

class SystemSettingListAPIView(APIView):
    """
    API endpoint for listing system settings.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        selector = SettingsSelector(request)
        settings = selector.get_system_settings()
        return Response(settings)
    
    def post(self, request):
        service = SettingsService(request)
        setting = service.create_system_setting(request.data)
        if setting:
            return Response(setting, status=status.HTTP_201_CREATED)
        return Response(
            {'error': 'Setting already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )


class SystemSettingDetailAPIView(APIView):
    """
    API endpoint for system setting details.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        selector = SettingsSelector(request)
        setting = selector.get_system_setting(pk)
        if setting:
            return Response(setting)
        return Response({'error': 'Setting not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        service = SettingsService(request)
        setting = service.update_system_setting(pk, request.data)
        if setting:
            return Response(setting)
        return Response({'error': 'Setting not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        service = SettingsService(request)
        success = service.delete_system_setting(pk)
        if success:
            return Response({'message': 'Setting deleted successfully'})
        return Response({'error': 'Setting not found'}, status=status.HTTP_404_NOT_FOUND)
