"""
URLs for CRM module
"""
from django.urls import path
from .views import (
    # Customer views
    CustomerListView, CustomerDetailView, CustomerCreateView, CustomerUpdateView, CustomerDeleteView,
    # Device views
    DeviceListView, DeviceDetailView, DeviceCreateView, DeviceUpdateView, DeviceDeleteView,
    # Type views
    CustomerTypeListView, CustomerTypeCreateView, CustomerTypeUpdateView, CustomerTypeDeleteView,
    # Brand views
    DeviceBrandListView, DeviceBrandCreateView, DeviceBrandUpdateView, DeviceBrandDeleteView,
    # Model views
    DeviceModelListView,
    # Quick create
    quick_create_customer,
)

app_name = 'crm'

urlpatterns = [
    # Customer URLs
    path('customers/', CustomerListView.as_view(), name='customer_list'),
    path('customers/create/', CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<uuid:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
    path('customers/<uuid:pk>/edit/', CustomerUpdateView.as_view(), name='customer_edit'),
    path('customers/<uuid:pk>/delete/', CustomerDeleteView.as_view(), name='customer_delete'),
    
    # Device URLs
    path('devices/', DeviceListView.as_view(), name='device_list'),
    path('devices/create/', DeviceCreateView.as_view(), name='device_create'),
    path('devices/<uuid:pk>/', DeviceDetailView.as_view(), name='device_detail'),
    path('devices/<uuid:pk>/edit/', DeviceUpdateView.as_view(), name='device_edit'),
    path('devices/<uuid:pk>/delete/', DeviceDeleteView.as_view(), name='device_delete'),
    
    # Customer Type URLs
    path('customer-types/', CustomerTypeListView.as_view(), name='customertype_list'),
    path('customer-types/create/', CustomerTypeCreateView.as_view(), name='customertype_create'),
    path('customer-types/<uuid:pk>/edit/', CustomerTypeUpdateView.as_view(), name='customertype_edit'),
    path('customer-types/<uuid:pk>/delete/', CustomerTypeDeleteView.as_view(), name='customertype_delete'),
    
    # Device Brand URLs
    path('device-brands/', DeviceBrandListView.as_view(), name='devicebrand_list'),
    path('device-brands/create/', DeviceBrandCreateView.as_view(), name='devicebrand_create'),
    path('device-brands/<uuid:pk>/edit/', DeviceBrandUpdateView.as_view(), name='devicebrand_edit'),
    path('device-brands/<uuid:pk>/delete/', DeviceBrandDeleteView.as_view(), name='devicebrand_delete'),
    
    # Device Model URLs
    path('device-models/', DeviceModelListView.as_view(), name='devicemodel_list'),
    
    # Quick creation
    path('customers/quick-create/', quick_create_customer, name='quick_create_customer'),
]
