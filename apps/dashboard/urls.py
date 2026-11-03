"""
URLs for the dashboard application.
"""
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Frontend URLs
    path('', views.dashboard_view, name='dashboard'),
]

# API URLs
urlpatterns_api = [
    path('stats/', views.DashboardStatsAPIView.as_view(), name='api_stats'),
    path('recent-activity/', views.RecentActivityAPIView.as_view(), name='api_recent_activity'),
]
