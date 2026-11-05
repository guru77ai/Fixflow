"""
API URLs for CRM module
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    CustomerTypeViewSet, CustomerSourceViewSet, CustomerGroupViewSet,
    DeviceCategoryViewSet, DeviceBrandViewSet, DeviceModelViewSet,
    CustomerViewSet, DeviceViewSet, CustomerCommunicationViewSet,
    CustomerDocumentViewSet
)

router = DefaultRouter()

# Customer Type, Source, Group
router.register(r'customer-types', CustomerTypeViewSet, basename='customertype')
router.register(r'customer-sources', CustomerSourceViewSet, basename='customersource')
router.register(r'customer-groups', CustomerGroupViewSet, basename='customergroup')

# Device Category, Brand, Model
router.register(r'device-categories', DeviceCategoryViewSet, basename='devicecategory')
router.register(r'device-brands', DeviceBrandViewSet, basename='devicebrand')
router.register(r'device-models', DeviceModelViewSet, basename='devicemodel')

# Main entities
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'devices', DeviceViewSet, basename='device')
router.register(r'communications', CustomerCommunicationViewSet, basename='communication')
router.register(r'documents', CustomerDocumentViewSet, basename='document')

urlpatterns = [
    path('', include(router.urls)),
]
