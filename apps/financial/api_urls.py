"""
API URLs for Financial module
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    InvoiceStatusViewSet, InvoiceTypeViewSet, InvoiceViewSet,
    InvoiceItemViewSet, InvoicePaymentViewSet, PaymentViewSet,
    ExpenseViewSet, ExpenseCategoryViewSet,
    ExpenseAttachmentViewSet, FinancialReportViewSet
)

router = DefaultRouter()

router.register(r'invoice-statuses', InvoiceStatusViewSet, basename='invoicestatus')
router.register(r'invoice-types', InvoiceTypeViewSet, basename='invoicetype')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'invoice-items', InvoiceItemViewSet, basename='invoiceitem')
router.register(r'invoice-payments', InvoicePaymentViewSet, basename='invoicepayment')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'expense-categories', ExpenseCategoryViewSet, basename='expensecategory')
router.register(r'expense-attachments', ExpenseAttachmentViewSet, basename='expenseattachment')
router.register(r'financial-reports', FinancialReportViewSet, basename='financialreport')

urlpatterns = [
    path('', include(router.urls)),
]
