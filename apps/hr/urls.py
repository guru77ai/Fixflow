"""
URLs for HR module
"""
from django.urls import path
from .views import DashboardView

app_name = 'hr'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
]
