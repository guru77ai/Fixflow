"""
API URLs for Financial module
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    InvoiceStatusViewSet, InvoiceTypeViewSet, InvoiceViewSet,
    InvoiceItemViewSet, InvoicePaymentViewSet, PaymentViewSet,
    PaymentMethodViewSet, ExpenseViewSet, ExpenseCategoryViewSet,
    TaxRateViewSet, BudgetCategoryViewSet, BudgetViewSet,
    CurrencyViewSet
)

router = DefaultRouter()

router.register(r'invoice-statuses', InvoiceStatusViewSet, basename='invoicestatus')
router.register(r'invoice-types', InvoiceTypeViewSet, basename='invoicetype')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'invoice-items', InvoiceItemViewSet, basename='invoiceitem')
router.register(r'invoice-payments', InvoicePaymentViewSet, basename='invoicepayment')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'payment-methods', PaymentMethodViewSet, basename='paymentmethod')
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'expense-categories', ExpenseCategoryViewSet, basename='expensecategory')
router.register(r'tax-rates', TaxRateViewSet, basename='taxrate')
router.register(r'budget-categories', BudgetCategoryViewSet, basename='budgetcategory')
router.register(r'budgets', BudgetViewSet, basename='budget')
router.register(r'currencies', CurrencyViewSet, basename='currency')

urlpatterns = [
    path('', include(router.urls)),
]
