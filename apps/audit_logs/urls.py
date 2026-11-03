"""
URLs for the audit_logs application.
"""
from django.urls import path
from . import views

app_name = 'audit_logs'

urlpatterns = [
    # API URLs
    path('', views.AuditLogListAPIView.as_view(), name='api_list'),
    path('<uuid:pk>/', views.AuditLogDetailAPIView.as_view(), name='api_detail'),
]
