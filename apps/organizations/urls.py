"""
URLs for the organizations application.
"""
from django.urls import path
from . import views

app_name = 'organizations'

urlpatterns = [
    # API URLs
    path('', views.OrganizationListAPIView.as_view(), name='api_list'),
    path('<uuid:pk>/', views.OrganizationDetailAPIView.as_view(), name='api_detail'),
]
