"""
Views for the barcode application.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .services import BarcodeService
from .selectors import BarcodeSelector


# Frontend Views

@login_required
def barcode_generator_view(request):
    """
    Barcode generator view.
    """
    if request.method == 'POST':
        data = request.POST.get('data', '')
        barcode_type = request.POST.get('barcode_type', 'code128')
        
        service = BarcodeService()
        barcode_image = service.generate_barcode(data, barcode_type)
        
        context = {
            'page_title': _('Barcode Generator'),
            'data': data,
            'barcode_type': barcode_type,
            'barcode_image': barcode_image,
        }
        
        return render(request, 'barcode/generator.html', context)
    
    context = {
        'page_title': _('Barcode Generator'),
    }
    
    return render(request, 'barcode/generator.html', context)


@login_required
def barcode_print_view(request):
    """
    Barcode print view.
    """
    context = {
        'page_title': _('Print Barcodes'),
    }
    
    return render(request, 'barcode/print.html', context)


# API Views

class BarcodeGenerateAPIView(APIView):
    """
    API endpoint for generating barcodes.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        data = request.data.get('data', '')
        barcode_type = request.data.get('barcode_type', 'code128')
        
        service = BarcodeService()
        barcode_image = service.generate_barcode(data, barcode_type)
        
        if barcode_image:
            return Response({
                'data': data,
                'barcode_type': barcode_type,
                'image': barcode_image
            })
        
        return Response(
            {'error': 'Failed to generate barcode'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
