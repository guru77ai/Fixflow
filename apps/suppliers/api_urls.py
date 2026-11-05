"""
API URLs for Suppliers module
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    SupplierCategoryViewSet, SupplierViewSet,
    SupplierContactViewSet, SupplierDocumentViewSet
)

router = DefaultRouter()

router.register(r'supplier-categories', SupplierCategoryViewSet, basename='suppliercategory')
router.register(r'suppliers', SupplierViewSet, basename='supplier')
router.register(r'supplier-contacts', SupplierContactViewSet, basename='suppliercontact')
router.register(r'supplier-documents', SupplierDocumentViewSet, basename='supplierdocument')

urlpatterns = [
    path('', include(router.urls)),
]
