"""
API URLs for Accounting module
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    AccountTypeViewSet, AccountCategoryViewSet, ChartOfAccountsViewSet,
    AccountViewSet, JournalEntryViewSet, JournalEntryLineViewSet,
    LedgerViewSet, BankAccountViewSet, BankTransactionViewSet,
    TrialBalanceViewSet, FinancialStatementViewSet
)

router = DefaultRouter()

router.register(r'account-types', AccountTypeViewSet, basename='accounttype')
router.register(r'account-categories', AccountCategoryViewSet, basename='accountcategory')
router.register(r'chart-of-accounts', ChartOfAccountsViewSet, basename='chartofaccounts')
router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'journal-entries', JournalEntryViewSet, basename='journalentry')
router.register(r'journal-entry-lines', JournalEntryLineViewSet, basename='journalentryline')
router.register(r'ledger', LedgerViewSet, basename='ledger')
router.register(r'bank-accounts', BankAccountViewSet, basename='bankaccount')
router.register(r'bank-transactions', BankTransactionViewSet, basename='banktransaction')
router.register(r'trial-balances', TrialBalanceViewSet, basename='trialbalance')
router.register(r'financial-statements', FinancialStatementViewSet, basename='financialstatement')

urlpatterns = [
    path('', include(router.urls)),
]
