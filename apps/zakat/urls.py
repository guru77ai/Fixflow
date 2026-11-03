"""
URLs for the zakat application.
"""
from django.urls import path
from . import views

app_name = 'zakat'

urlpatterns = [
    # API URLs
    path('calculate/', views.ZakatCalculateAPIView.as_view(), name='api_calculate'),
    path('history/', views.ZakatHistoryAPIView.as_view(), name='api_history'),
]
