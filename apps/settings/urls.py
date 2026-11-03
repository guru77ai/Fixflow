"""
URLs for the settings application.
"""
from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    # API URLs
    path('system/', views.SystemSettingListAPIView.as_view(), name='api_system_settings'),
    path('system/<uuid:pk>/', views.SystemSettingDetailAPIView.as_view(), name='api_system_setting_detail'),
]
