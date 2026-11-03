"""
URLs for the branches application.
"""
from django.urls import path
from . import views

app_name = 'branches'

urlpatterns = [
    # API URLs
    path('', views.BranchListAPIView.as_view(), name='api_list'),
    path('<uuid:pk>/', views.BranchDetailAPIView.as_view(), name='api_detail'),
]
