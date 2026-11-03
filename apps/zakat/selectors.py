"""
Selectors for the zakat application.
"""
from django.db.models import Q
from .models import ZakatCalculation, ZakatSettings, ZakatPayment


class ZakatSelector:
    """
    Selector for zakat queries.
    """
    
    def __init__(self, request):
        self.request = request
        self.user = request.user
        self.organization = getattr(request, 'current_organization', None)
    
    def get_zakat_data(self):
        """
        Get zakat calculation data.
        """
        data = {
            'settings': self.get_zakat_settings(),
            'calculations': self.get_zakat_calculations()[:5],
            'payments': self.get_zakat_payments()[:5],
        }
        return data
    
    def get_zakat_settings(self):
        """
        Get zakat settings for the organization.
        """
        try:
            settings = ZakatSettings.objects.get(organization=self.organization)
            return self.get_zakat_settings_data(settings)
        except ZakatSettings.DoesNotExist:
            return None
    
    def get_zakat_calculations(self, **filters):
        """
        Get a list of zakat calculations.
        """
        queryset = ZakatCalculation.objects.filter(organization=self.organization)
        
        # Apply filters
        if 'start_date' in filters:
            queryset = queryset.filter(start_date__gte=filters['start_date'])
        
        if 'end_date' in filters:
            queryset = queryset.filter(end_date__lte=filters['end_date'])
        
        if 'calculation_method' in filters:
            queryset = queryset.filter(calculation_method=filters['calculation_method'])
        
        if 'search' in filters and filters['search']:
            search = filters['search']
            queryset = queryset.filter(
                Q(notes__icontains=search)
            )
        
        return [
            self.get_zakat_calculation_data(calc) for calc in queryset.order_by('-created_at')
        ]
    
    def get_zakat_calculation(self, pk):
        """
        Get a zakat calculation by ID.
        """
        try:
            calc = ZakatCalculation.objects.get(pk=pk, organization=self.organization)
            return self.get_zakat_calculation_data(calc)
        except ZakatCalculation.DoesNotExist:
            return None
    
    def get_zakat_payments(self, **filters):
        """
        Get a list of zakat payments.
        """
        queryset = ZakatPayment.objects.filter(organization=self.organization)
        
        # Apply filters
        if 'start_date' in filters:
            queryset = queryset.filter(payment_date__gte=filters['start_date'])
        
        if 'end_date' in filters:
            queryset = queryset.filter(payment_date__lte=filters['end_date'])
        
        if 'payment_method' in filters:
            queryset = queryset.filter(payment_method=filters['payment_method'])
        
        if 'search' in filters and filters['search']:
            search = filters['search']
            queryset = queryset.filter(
                Q(recipient__icontains=search) |
                Q(reference__icontains=search) |
                Q(notes__icontains=search)
            )
        
        return [
            self.get_zakat_payment_data(payment) for payment in queryset.order_by('-payment_date')
        ]
    
    def get_zakat_payment(self, pk):
        """
        Get a zakat payment by ID.
        """
        try:
            payment = ZakatPayment.objects.get(pk=pk, organization=self.organization)
            return self.get_zakat_payment_data(payment)
        except ZakatPayment.DoesNotExist:
            return None
    
    def get_zakat_history(self):
        """
        Get zakat calculation and payment history.
        """
        history = []
        
        # Add calculations
        for calc in self.get_zakat_calculations():
            history.append({
                'type': 'calculation',
                'data': calc,
                'date': calc['created_at']
            })
        
        # Add payments
        for payment in self.get_zakat_payments():
            history.append({
                'type': 'payment',
                'data': payment,
                'date': payment['payment_date']
            })
        
        # Sort by date
        history.sort(key=lambda x: x['date'], reverse=True)
        
        return history
    
    def get_zakat_settings_data(self, settings):
        """
        Get zakat settings data for responses.
        """
        return {
            'id': str(settings.id),
            'organization': {
                'id': str(settings.organization.id),
                'name': settings.organization.name,
            },
            'default_nisab_threshold': float(settings.default_nisab_threshold),
            'default_zakat_rate': float(settings.default_zakat_rate),
            'default_calculation_method': settings.default_calculation_method,
            'include_cash': settings.include_cash,
            'include_inventory': settings.include_inventory,
            'include_receivables': settings.include_receivables,
            'include_financial_assets': settings.include_financial_assets,
            'deduct_payables': settings.deduct_payables,
            'deduct_loans': settings.deduct_loans,
            'created_at': settings.created_at.isoformat(),
            'updated_at': settings.updated_at.isoformat(),
        }
    
    def get_zakat_calculation_data(self, calc):
        """
        Get zakat calculation data for responses.
        """
        return {
            'id': str(calc.id),
            'calculation_method': calc.calculation_method,
            'calculation_method_display': calc.get_calculation_method_display(),
            'start_date': calc.start_date.isoformat(),
            'end_date': calc.end_date.isoformat(),
            'eligible_cash': float(calc.eligible_cash),
            'eligible_inventory': float(calc.eligible_inventory),
            'eligible_receivables': float(calc.eligible_receivables),
            'eligible_financial_assets': float(calc.eligible_financial_assets),
            'total_eligible_assets': float(calc.total_eligible_assets),
            'deductible_liabilities': float(calc.deductible_liabilities),
            'net_eligible_assets': float(calc.net_eligible_assets),
            'nisab_threshold': float(calc.nisab_threshold),
            'zakat_rate': float(calc.zakat_rate),
            'zakat_amount': float(calc.zakat_amount),
            'nisab_met': calc.net_eligible_assets >= calc.nisab_threshold,
            'notes': calc.notes,
            'calculated_by': {
                'id': str(calc.calculated_by.id) if calc.calculated_by else None,
                'email': calc.calculated_by.email if calc.calculated_by else None,
            } if calc.calculated_by else None,
            'created_at': calc.created_at.isoformat(),
        }
    
    def get_zakat_payment_data(self, payment):
        """
        Get zakat payment data for responses.
        """
        return {
            'id': str(payment.id),
            'calculation': {
                'id': str(payment.calculation.id) if payment.calculation else None,
                'zakat_amount': float(payment.calculation.zakat_amount) if payment.calculation else 0,
            } if payment.calculation else None,
            'organization': {
                'id': str(payment.organization.id),
                'name': payment.organization.name,
            },
            'amount': float(payment.amount),
            'currency': payment.currency,
            'payment_method': payment.payment_method,
            'payment_method_display': payment.get_payment_method_display(),
            'payment_date': payment.payment_date.isoformat(),
            'reference': payment.reference,
            'recipient': payment.recipient,
            'notes': payment.notes,
            'recorded_by': {
                'id': str(payment.recorded_by.id) if payment.recorded_by else None,
                'email': payment.recorded_by.email if payment.recorded_by else None,
            } if payment.recorded_by else None,
            'created_at': payment.created_at.isoformat(),
        }
