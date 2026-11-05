"""
Selectors for POS module
"""
from django.db.models import Q, Sum, Count
from django.utils import timezone
from .models import Sale, SaleItem, SalePayment, Receipt, Refund, CashRegister, POSSession


class SaleSelector:
    @staticmethod
    def get_all_sales(organization, branch=None, status=None, customer=None, search=None, start_date=None, end_date=None):
        queryset = Sale.objects.filter(organization=organization)
        if branch: queryset = queryset.filter(branch=branch)
        if status: queryset = queryset.filter(status=status)
        if customer: queryset = queryset.filter(customer=customer)
        if start_date: queryset = queryset.filter(created_at__gte=start_date)
        if end_date: queryset = queryset.filter(created_at__lte=end_date)
        if search:
            queryset = queryset.filter(
                Q(sale_number__icontains=search) |
                Q(customer__first_name__icontains=search) |
                Q(customer__last_name__icontains=search)
            )
        return queryset.order_by('-created_at')
    
    @staticmethod
    def get_daily_sales(organization, branch=None, date=None):
        if date is None:
            date = timezone.now().date()
        return Sale.objects.filter(
            organization=organization,
            created_at__date=date
        ).order_by('-created_at')
    
    @staticmethod
    def get_statistics(organization, branch=None):
        queryset = Sale.objects.filter(organization=organization)
        if branch: queryset = queryset.filter(branch=branch)
        
        return {
            'total': queryset.count(),
            'total_sales': queryset.aggregate(total=Sum('total_amount'))['total'] or 0,
            'total_paid': queryset.aggregate(total=Sum('amount_paid'))['total'] or 0,
            'total_outstanding': queryset.aggregate(total=Sum('balance'))['total'] or 0,
            'by_status': list(queryset.values('status').annotate(count=Count('id'))),
        }


class CashRegisterSelector:
    @staticmethod
    def get_all_registers(organization, branch=None, is_active=True):
        queryset = CashRegister.objects.filter(organization=organization)
        if branch: queryset = queryset.filter(branch=branch)
        if is_active: queryset = queryset.filter(is_active=True)
        return queryset.order_by('name')
    
    @staticmethod
    def get_open_registers(organization, branch=None):
        return CashRegister.objects.filter(
            organization=organization,
            is_open=True
        ).order_by('name')


class POSSessionSelector:
    @staticmethod
    def get_all_sessions(organization, branch=None, user=None, is_active=None):
        queryset = POSSession.objects.filter(organization=organization)
        if branch: queryset = queryset.filter(branch=branch)
        if user: queryset = queryset.filter(user=user)
        if is_active is not None: queryset = queryset.filter(is_active=is_active)
        return queryset.order_by('-started_at')


class PaymentMethodSelector:
    @staticmethod
    def get_all_methods(active_only=True):
        queryset = PaymentMethod.objects.all()
        if active_only: queryset = queryset.filter(is_active=True)
        return queryset.order_by('name')
