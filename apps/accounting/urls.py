"""
URLs for Accounting module
"""
from django.urls import path
from .views import DashboardView

app_name = 'accounting'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
]
