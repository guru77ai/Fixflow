"""
URLs for POS module
"""
from django.urls import path
from .views import SaleListView, SaleDetailView, SaleCreateView, POSDashboardView, SaleAPIView

app_name = 'pos'

urlpatterns = [
    path('', POSDashboardView.as_view(), name='dashboard'),
    path('sales/', SaleListView.as_view(), name='sale_list'),
    path('sales/create/', SaleCreateView.as_view(), name='sale_create'),
    path('sales/<uuid:pk>/', SaleDetailView.as_view(), name='sale_detail'),
    
    # API - These are function-based views, need to be wrapped properly
    # path('api/sales/', SaleAPIView.as_view(), name='sale_api_list'),
    # path('api/sales/<uuid:pk>/', SaleAPIView.as_view(), name='sale_api_detail'),
]
