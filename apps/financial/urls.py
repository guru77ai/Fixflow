"""
URLs for Financial module
"""
from django.urls import path
from .views import DashboardView

app_name = 'financial'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
]
