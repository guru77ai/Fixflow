"""
URLs for the accounts application.
"""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # API URLs
    path('me/', views.UserAPIView.as_view(), name='api_me'),
    path('users/', views.UserListAPIView.as_view(), name='api_users'),
]
