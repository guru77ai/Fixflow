"""
URLs for the backups application.
"""
from django.urls import path
from . import views

app_name = 'backups'

urlpatterns = [
    # API URLs
    path('', views.BackupListAPIView.as_view(), name='api_list'),
    path('<uuid:pk>/', views.BackupDetailAPIView.as_view(), name='api_detail'),
]
