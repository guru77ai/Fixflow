"""
Services for the dashboard application.
"""
from django.utils import timezone
from decimal import Decimal


class DashboardService:
    """
    Service for dashboard data processing.
    """
    
    def __init__(self, request):
        self.request = request
        self.user = request.user
        self.organization = getattr(request, 'current_organization', None)
        self.branch = getattr(request, 'current_branch', None)
    
    def get_dashboard_data(self):
        """
        Get all dashboard data.
        """
        data = {
            'stats': self.get_stats(),
            'recent_activity': self.get_recent_activity(),
            'charts': self.get_chart_data(),
        }
        return data
    
    def get_stats(self):
        """
        Get dashboard statistics.
        """
        from .selectors import DashboardSelector
        selector = DashboardSelector(self.request)
        return selector.get_stats()
    
    def get_recent_activity(self):
        """
        Get recent activity.
        """
        from .selectors import DashboardSelector
        selector = DashboardSelector(self.request)
        return selector.get_recent_activity()
    
    def get_chart_data(self):
        """
        Get chart data.
        """
        from .selectors import DashboardSelector
        selector = DashboardSelector(self.request)
        return selector.get_chart_data()
