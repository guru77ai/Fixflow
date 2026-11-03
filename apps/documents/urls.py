"""
URLs for the documents application.
"""
from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    # API URLs
    path('', views.DocumentListAPIView.as_view(), name='api_list'),
    path('<uuid:pk>/', views.DocumentDetailAPIView.as_view(), name='api_detail'),
]
