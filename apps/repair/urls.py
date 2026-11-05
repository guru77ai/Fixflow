"""
URLs for Repair module
"""
from django.urls import path
from .views import (
    # Repair Order views
    RepairOrderListView, RepairOrderDetailView, RepairOrderCreateView,
    RepairOrderUpdateView, RepairOrderDeleteView, RepairOrderStatusChangeView,
    # Dashboard
    RepairDashboardView,
    # API views
    RepairOrderAPIView, RepairStatisticsAPIView,
    quick_create_repair_order,
    # Search
    RepairOrderSearchView, DeviceSearchForRepairView,
)

app_name = 'repair'

urlpatterns = [
    # Dashboard
    path('', RepairDashboardView.as_view(), name='dashboard'),
    
    # Repair Order URLs
    path('orders/', RepairOrderListView.as_view(), name='repairorder_list'),
    path('orders/create/', RepairOrderCreateView.as_view(), name='repairorder_create'),
    path('orders/<uuid:pk>/', RepairOrderDetailView.as_view(), name='repairorder_detail'),
    path('orders/<uuid:pk>/edit/', RepairOrderUpdateView.as_view(), name='repairorder_update'),
    path('orders/<uuid:pk>/delete/', RepairOrderDeleteView.as_view(), name='repairorder_delete'),
    path('orders/<uuid:pk>/status/', RepairOrderStatusChangeView.as_view(), name='repairorder_status_change'),
    
    # API URLs
    path('api/orders/', RepairOrderAPIView.as_view(), name='repairorder_api_list'),
    path('api/orders/<uuid:pk>/', RepairOrderAPIView.as_view(), name='repairorder_api_detail'),
    path('api/statistics/', RepairStatisticsAPIView.as_view(), name='repair_statistics_api'),
    
    # Quick creation
    path('api/orders/quick-create/', quick_create_repair_order, name='quick_create_repair_order'),
    
    # Search
    path('api/orders/search/', RepairOrderSearchView.as_view(), name='repairorder_search'),
    path('api/devices/search/', DeviceSearchForRepairView.as_view(), name='device_search_for_repair'),
]
