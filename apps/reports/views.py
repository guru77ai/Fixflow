"""
Views for the reports application.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .services import ReportService
from .selectors import ReportSelector


# Frontend Views

@login_required
def report_dashboard_view(request):
    """
    Reports dashboard view.
    """
    selector = ReportSelector(request)
    report_data = selector.get_report_dashboard()
    
    context = {
        'page_title': _('Reports Dashboard'),
        'report_data': report_data,
    }
    
    return render(request, 'reports/dashboard.html', context)


@login_required
def sales_report_view(request):
    """
    Sales report view.
    """
    selector = ReportSelector(request)
    sales_data = selector.get_sales_report()
    
    context = {
        'page_title': _('Sales Report'),
        'sales_data': sales_data,
    }
    
    return render(request, 'reports/sales.html', context)


@login_required
def repair_report_view(request):
    """
    Repair report view.
    """
    selector = ReportSelector(request)
    repair_data = selector.get_repair_report()
    
    context = {
        'page_title': _('Repair Report'),
        'repair_data': repair_data,
    }
    
    return render(request, 'reports/repairs.html', context)


@login_required
def inventory_report_view(request):
    """
    Inventory report view.
    """
    selector = ReportSelector(request)
    inventory_data = selector.get_inventory_report()
    
    context = {
        'page_title': _('Inventory Report'),
        'inventory_data': inventory_data,
    }
    
    return render(request, 'reports/inventory.html', context)


@login_required
def financial_report_view(request):
    """
    Financial report view.
    """
    selector = ReportSelector(request)
    financial_data = selector.get_financial_report()
    
    context = {
        'page_title': _('Financial Report'),
        'financial_data': financial_data,
    }
    
    return render(request, 'reports/financial.html', context)


# API Views

class ReportDashboardAPIView(APIView):
    """
    API endpoint for reports dashboard.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        selector = ReportSelector(request)
        report_data = selector.get_report_dashboard()
        return Response(report_data)


class SalesReportAPIView(APIView):
    """
    API endpoint for sales report.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        selector = ReportSelector(request)
        sales_data = selector.get_sales_report()
        return Response(sales_data)


class RepairReportAPIView(APIView):
    """
    API endpoint for repair report.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        selector = ReportSelector(request)
        repair_data = selector.get_repair_report()
        return Response(repair_data)


class InventoryReportAPIView(APIView):
    """
    API endpoint for inventory report.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        selector = ReportSelector(request)
        inventory_data = selector.get_inventory_report()
        return Response(inventory_data)


class FinancialReportAPIView(APIView):
    """
    API endpoint for financial report.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        selector = ReportSelector(request)
        financial_data = selector.get_financial_report()
        return Response(financial_data)
