"""
API URLs for POS module
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    PaymentMethodViewSet, CashRegisterViewSet, SaleViewSet,
    SaleItemViewSet, SalePaymentViewSet, ReceiptViewSet,
    RefundViewSet, RefundItemViewSet, POSSessionViewSet,
    POSSettingsViewSet
)

router = DefaultRouter()

router.register(r'payment-methods', PaymentMethodViewSet, basename='paymentmethod')
router.register(r'cash-registers', CashRegisterViewSet, basename='cashregister')
router.register(r'sales', SaleViewSet, basename='sale')
router.register(r'sale-items', SaleItemViewSet, basename='saleitem')
router.register(r'sale-payments', SalePaymentViewSet, basename='salepayment')
router.register(r'receipts', ReceiptViewSet, basename='receipt')
router.register(r'refunds', RefundViewSet, basename='refund')
router.register(r'refund-items', RefundItemViewSet, basename='refunditem')
router.register(r'pos-sessions', POSSessionViewSet, basename='possession')
router.register(r'pos-settings', POSSettingsViewSet, basename='possettings')

urlpatterns = [
    path('', include(router.urls)),
]
