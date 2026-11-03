"""
URLs for the barcode application.
"""
from django.urls import path
from . import views

app_name = 'barcode'

urlpatterns = [
    # API URLs
    path('generate/', views.BarcodeGenerateAPIView.as_view(), name='api_generate'),
]
