"""
API Views for Accounting module
"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    AccountType, AccountCategory, ChartOfAccounts, Account,
    JournalEntry, JournalEntryLine, Ledger, BankAccount,
    BankTransaction, TrialBalance, FinancialStatement
)
from .serializers import (
    AccountTypeSerializer, AccountCategorySerializer, ChartOfAccountsSerializer,
    AccountSerializer, JournalEntrySerializer, JournalEntryLineSerializer,
    LedgerSerializer, BankAccountSerializer, BankTransactionSerializer,
    TrialBalanceSerializer, FinancialStatementSerializer
)
from apps.core.pagination import StandardResultsSetPagination
from apps.core.api_mixins import TenantScopedMixin


class AccountTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """Global reference data: not tenant-scoped"""
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['normal_balance']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code']
    pagination_class = StandardResultsSetPagination


class AccountCategoryViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch"""
    queryset = AccountCategory.objects.all()
    serializer_class = AccountCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['account_type', 'parent', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'sequence']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.filter_by_tenant(super().get_queryset())


class ChartOfAccountsViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch"""
    queryset = ChartOfAccounts.objects.all()
    serializer_class = ChartOfAccountsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'is_default']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.filter_by_tenant(super().get_queryset())


class AccountViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch"""
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['account_type', 'category', 'status', 'is_active', 'is_bank', 'is_cash']
    search_fields = ['code', 'name', 'description']
    ordering_fields = ['code', 'name', 'current_balance']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.filter_by_tenant(super().get_queryset())


class JournalEntryViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch"""
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_posted', 'entry_date', 'created_by', 'approved_by']
    search_fields = ['entry_number', 'reference', 'description']
    ordering_fields = ['entry_number', 'entry_date', 'created_at']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.filter_by_tenant(super().get_queryset())
    
    @action(detail=True, methods=['get'])
    def lines(self, request, pk=None):
        entry = self.get_object()
        self.validate_tenant(entry)
        lines = entry.lines.all()
        serializer = JournalEntryLineSerializer(lines, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def post(self, request, pk=None):
        """
        Post a journal entry to the ledger.
        
        Validates:
        - Entry belongs to current tenant
        - Entry is not already posted
        - Entry has lines
        - Debits equal credits (balanced)
        - All accounts are valid and active
        - User has permission to post
        """
        from .services import JournalEntryService
        from rest_framework.exceptions import PermissionDenied, ValidationError
        from decimal import Decimal
        
        entry = self.get_object()
        self.validate_tenant(entry)
        
        # Validate entry is not already posted
        if entry.is_posted:
            raise ValidationError({'error': 'Journal entry is already posted'})
        
        # Validate entry has lines
        if not entry.lines.exists():
            raise ValidationError({'error': 'Cannot post journal entry with no lines'})
        
        # Validate all accounts belong to the same organization
        for line in entry.lines.all():
            if line.account.organization_id != entry.organization_id:
                raise PermissionDenied('Journal entry line references an account from another organization')
            if not line.account.is_active:
                raise ValidationError({'error': f'Account {line.account.code} is inactive'})
        
        # Validate debits equal credits
        total_debit = sum(Decimal(line.debit) for line in entry.lines.all())
        total_credit = sum(Decimal(line.credit) for line in entry.lines.all())
        
        if total_debit != total_credit:
            raise ValidationError({
                'error': 'Journal entry is not balanced',
                'details': f'Total debit ({total_debit}) does not equal total credit ({total_credit})'
            })
        
        # Use domain service to post
        try:
            JournalEntryService.post_to_ledger(entry)
        except Exception as e:
            raise ValidationError({'error': f'Failed to post journal entry: {str(e)}'})
        
        serializer = JournalEntrySerializer(entry, context={'request': request})
        return Response(serializer.data)


class JournalEntryLineViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch (via journal_entry relationship)"""
    queryset = JournalEntryLine.objects.all()
    serializer_class = JournalEntryLineSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['journal_entry', 'account']
    ordering_fields = ['debit', 'credit']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by tenant via journal_entry relationship
        org = self.get_organization()
        branch = self.get_branch()
        return queryset.filter(
            journal_entry__organization=org,
            journal_entry__branch=branch
        ).distinct()


class LedgerViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch"""
    queryset = Ledger.objects.all()
    serializer_class = LedgerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['account', 'entry_date', 'created_by']
    search_fields = ['account__code', 'account__name', 'reference', 'description']
    ordering_fields = ['entry_date', 'created_at']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.filter_by_tenant(super().get_queryset())


class BankAccountViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch"""
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['bank_name', 'is_active']
    search_fields = ['bank_name', 'account_number', 'account_holder']
    ordering_fields = ['bank_name', 'account_number', 'current_balance']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.filter_by_tenant(super().get_queryset())
    
    @action(detail=True, methods=['get'])
    def transactions(self, request, pk=None):
        bank_account = self.get_object()
        self.validate_tenant(bank_account)
        transactions = bank_account.transactions.all()
        serializer = BankTransactionSerializer(transactions, many=True, context={'request': request})
        return Response(serializer.data)


class BankTransactionViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch"""
    queryset = BankTransaction.objects.all()
    serializer_class = BankTransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['bank_account', 'transaction_type', 'transaction_date', 'is_reconciled']
    search_fields = ['transaction_number', 'reference', 'description']
    ordering_fields = ['transaction_number', 'transaction_date', 'amount']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.filter_by_tenant(super().get_queryset())


class TrialBalanceViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch"""
    queryset = TrialBalance.objects.all()
    serializer_class = TrialBalanceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['period_start', 'period_end', 'account']
    ordering_fields = ['period_start', 'period_end', 'account__code']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.filter_by_tenant(super().get_queryset())


class FinancialStatementViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch"""
    queryset = FinancialStatement.objects.all()
    serializer_class = FinancialStatementSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['statement_type', 'period_start', 'period_end', 'generated_by']
    search_fields = ['name', 'statement_type']
    ordering_fields = ['name', 'period_start', 'created_at']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.filter_by_tenant(super().get_queryset())
