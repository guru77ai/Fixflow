"""
URLs for the licensing application.
"""
from django.urls import path
from . import views

app_name = 'licensing'

urlpatterns = [
    # API URLs
    path('verify/', views.LicenseVerifyAPIView.as_view(), name='api_verify'),
    path('status/', views.LicenseStatusAPIView.as_view(), name='api_status'),
]
