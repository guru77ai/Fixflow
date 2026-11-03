"""
Views for the zakat application.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .services import ZakatService
from .selectors import ZakatSelector


# Frontend Views

@login_required
def zakat_calculator_view(request):
    """
    Zakat calculator view.
    """
    selector = ZakatSelector(request)
    zakat_data = selector.get_zakat_data()
    
    if request.method == 'POST':
        # Calculate zakat based on form data
        service = ZakatService(request)
        calculation = service.calculate_zakat(request.POST)
        zakat_data['calculation'] = calculation
    
    context = {
        'page_title': _('Zakat Calculator'),
        'zakat_data': zakat_data,
    }
    
    return render(request, 'zakat/calculator.html', context)


@login_required
def zakat_report_view(request):
    """
    Zakat report view.
    """
    selector = ZakatSelector(request)
    zakat_history = selector.get_zakat_history()
    
    context = {
        'page_title': _('Zakat History'),
        'zakat_history': zakat_history,
    }
    
    return render(request, 'zakat/history.html', context)


# API Views

class ZakatCalculateAPIView(APIView):
    """
    API endpoint for zakat calculation.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        service = ZakatService(request)
        calculation = service.calculate_zakat(request.data)
        return Response(calculation)


class ZakatHistoryAPIView(APIView):
    """
    API endpoint for zakat history.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        selector = ZakatSelector(request)
        history = selector.get_zakat_history()
        return Response(history)
