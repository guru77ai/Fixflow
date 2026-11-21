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
    # Configuration views
    RepairStatusListView, RepairStatusCreateView, RepairStatusUpdateView, RepairStatusDeleteView,
    RepairPriorityListView, RepairPriorityCreateView, RepairPriorityUpdateView, RepairPriorityDeleteView,
    RepairCategoryListView, RepairCategoryCreateView, RepairCategoryUpdateView, RepairCategoryDeleteView,
    RepairTypeListView, RepairTypeCreateView, RepairTypeUpdateView, RepairTypeDeleteView,
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
    
    # API URLs - These are function-based views, need to be wrapped properly
    # path('api/orders/', RepairOrderAPIView.as_view(), name='repairorder_api_list'),
    # path('api/orders/<uuid:pk>/', RepairOrderAPIView.as_view(), name='repairorder_api_detail'),
    # path('api/statistics/', RepairStatisticsAPIView.as_view(), name='repair_statistics_api'),
    
    # Quick creation
    path('api/orders/quick-create/', quick_create_repair_order, name='quick_create_repair_order'),
    
    # Configuration URLs
    path('statuses/', RepairStatusListView.as_view(), name='repair_status_list'),
    path('statuses/create/', RepairStatusCreateView.as_view(), name='repair_status_create'),
    path('statuses/<uuid:pk>/edit/', RepairStatusUpdateView.as_view(), name='repair_status_update'),
    path('statuses/<uuid:pk>/delete/', RepairStatusDeleteView.as_view(), name='repair_status_delete'),
    
    path('priorities/', RepairPriorityListView.as_view(), name='repair_priority_list'),
    path('priorities/create/', RepairPriorityCreateView.as_view(), name='repair_priority_create'),
    path('priorities/<uuid:pk>/edit/', RepairPriorityUpdateView.as_view(), name='repair_priority_update'),
    path('priorities/<uuid:pk>/delete/', RepairPriorityDeleteView.as_view(), name='repair_priority_delete'),
    
    path('categories/', RepairCategoryListView.as_view(), name='repair_category_list'),
    path('categories/create/', RepairCategoryCreateView.as_view(), name='repair_category_create'),
    path('categories/<uuid:pk>/edit/', RepairCategoryUpdateView.as_view(), name='repair_category_update'),
    path('categories/<uuid:pk>/delete/', RepairCategoryDeleteView.as_view(), name='repair_category_delete'),
    
    path('types/', RepairTypeListView.as_view(), name='repair_type_list'),
    path('types/create/', RepairTypeCreateView.as_view(), name='repair_type_create'),
    path('types/<uuid:pk>/edit/', RepairTypeUpdateView.as_view(), name='repair_type_update'),
    path('types/<uuid:pk>/delete/', RepairTypeDeleteView.as_view(), name='repair_type_delete'),
    
    # Search - These are function-based views, need to be wrapped properly
    # path('api/orders/search/', RepairOrderSearchView.as_view(), name='repairorder_search'),
    # path('api/devices/search/', DeviceSearchForRepairView.as_view(), name='device_search_for_repair'),
]
