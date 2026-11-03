"""
Views for the dashboard application.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import DashboardService
from .selectors import DashboardSelector


@login_required
@login_required(redirect_field_name='next', login_url='login')
def dashboard_view(request):
    """
    Main dashboard view.
    """
    # Get dashboard data
    service = DashboardService(request)
    data = service.get_dashboard_data()
    
    # Breadcrumbs
    breadcrumbs = [
        {'name': _('Dashboard'), 'url': None}
    ]
    
    context = {
        'page_title': _('Dashboard'),
        'breadcrumbs': breadcrumbs,
        'stats': data.get('stats', {}),
        'recent_activity': data.get('recent_activity', []),
        'charts': data.get('charts', {}),
    }
    
    return render(request, 'dashboard/dashboard.html', context)


class DashboardStatsAPIView(APIView):
    """
    API endpoint for dashboard statistics.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        selector = DashboardSelector(request)
        stats = selector.get_stats()
        return Response(stats)


class RecentActivityAPIView(APIView):
    """
    API endpoint for recent activity.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        selector = DashboardSelector(request)
        activity = selector.get_recent_activity()
        return Response(activity)
