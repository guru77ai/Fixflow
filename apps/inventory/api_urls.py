"""
API URLs for Inventory module
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    WarehouseViewSet, ProductCategoryViewSet, ProductBrandViewSet,
    UnitOfMeasureViewSet, ProductViewSet, ProductSerialNumberViewSet,
    StockMovementViewSet, StockTransferViewSet, StockTransferItemViewSet,
    StockAdjustmentViewSet, StockAdjustmentItemViewSet,
    ServiceCategoryViewSet, ServiceViewSet
)

router = DefaultRouter()

# Warehouse, Category, Brand, UOM
router.register(r'warehouses', WarehouseViewSet, basename='warehouse')
router.register(r'product-categories', ProductCategoryViewSet, basename='productcategory')
router.register(r'product-brands', ProductBrandViewSet, basename='productbrand')
router.register(r'units-of-measure', UnitOfMeasureViewSet, basename='unitofmeasure')

# Products and Serial Numbers
router.register(r'products', ProductViewSet, basename='product')
router.register(r'product-serial-numbers', ProductSerialNumberViewSet, basename='productserialnumber')

# Stock Management
router.register(r'stock-movements', StockMovementViewSet, basename='stockmovement')
router.register(r'stock-transfers', StockTransferViewSet, basename='stocktransfer')
router.register(r'stock-transfer-items', StockTransferItemViewSet, basename='stocktransferitem')
router.register(r'stock-adjustments', StockAdjustmentViewSet, basename='stockadjustment')
router.register(r'stock-adjustment-items', StockAdjustmentItemViewSet, basename='stockadjustmentitem')

# Services
router.register(r'service-categories', ServiceCategoryViewSet, basename='servicecategory')
router.register(r'services', ServiceViewSet, basename='service')

urlpatterns = [
    path('', include(router.urls)),
]
