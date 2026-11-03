"""
Views for the licensing application.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import License, LicenseVerificationLog, Installation
from .services import LicenseService
from .selectors import LicenseSelector


# Frontend Views

@login_required
def license_view(request):
    """
    View license information.
    """
    selector = LicenseSelector(request)
    license_data = selector.get_license()
    
    context = {
        'page_title': _('License'),
        'license': license_data,
    }
    
    return render(request, 'licensing/view.html', context)


# API Views

class LicenseVerifyAPIView(APIView):
    """
    API endpoint for license verification.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        license_id = request.data.get('license_id')
        signature = request.data.get('signature')
        
        if not license_id or not signature:
            return Response(
                {'error': 'License ID and signature are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        service = LicenseService()
        result = service.verify_license(license_id, signature)
        
        if result.get('valid', False):
            return Response(result)
        else:
            return Response(
                {'error': result.get('error', 'Invalid license')},
                status=status.HTTP_403_FORBIDDEN
            )


class LicenseStatusAPIView(APIView):
    """
    API endpoint for license status.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        selector = LicenseSelector(request)
        license_data = selector.get_license()
        
        if license_data:
            return Response(license_data)
        else:
            return Response(
                {'error': 'No license found'},
                status=status.HTTP_404_NOT_FOUND
            )
