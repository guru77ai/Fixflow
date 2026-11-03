"""
Services for the reports application.
"""
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from decimal import Decimal


class ReportService:
    """
    Service for report operations.
    """
    
    def __init__(self, request):
        self.request = request
        self.user = request.user
    
    def get_report_data(self, report_type, **filters):
        """
        Get report data based on type.
        """
        selectors = {
            'dashboard': self.get_dashboard_data,
            'sales': self.get_sales_data,
            'repairs': self.get_repairs_data,
            'inventory': self.get_inventory_data,
            'financial': self.get_financial_data,
        }
        
        if report_type in selectors:
            return selectors[report_type](**filters)
        
        return {}
    
    def get_dashboard_data(self, **filters):
        """
        Get dashboard report data.
        """
        from .selectors import ReportSelector
        selector = ReportSelector(self.request)
        return selector.get_report_dashboard(**filters)
    
    def get_sales_data(self, **filters):
        """
        Get sales report data.
        """
        from .selectors import ReportSelector
        selector = ReportSelector(self.request)
        return selector.get_sales_report(**filters)
    
    def get_repairs_data(self, **filters):
        """
        Get repair report data.
        """
        from .selectors import ReportSelector
        selector = ReportSelector(self.request)
        return selector.get_repair_report(**filters)
    
    def get_inventory_data(self, **filters):
        """
        Get inventory report data.
        """
        from .selectors import ReportSelector
        selector = ReportSelector(self.request)
        return selector.get_inventory_report(**filters)
    
    def get_financial_data(self, **filters):
        """
        Get financial report data.
        """
        from .selectors import ReportSelector
        selector = ReportSelector(self.request)
        return selector.get_financial_report(**filters)
