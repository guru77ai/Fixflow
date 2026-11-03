"""
Services for the zakat application.
"""
from decimal import Decimal
from django.utils import timezone
from .models import ZakatCalculation, ZakatSettings, ZakatPayment


class ZakatService:
    """
    Service for zakat calculations and operations.
    """
    
    def __init__(self, request):
        self.request = request
        self.user = request.user
        self.organization = getattr(request, 'current_organization', None)
    
    def calculate_zakat(self, data):
        """
        Calculate zakat based on the provided data.
        """
        # Get or create zakat settings
        settings = self.get_zakat_settings()
        
        # Calculate eligible assets
        eligible_cash = Decimal(data.get('cash', '0'))
        eligible_inventory = Decimal(data.get('inventory', '0'))
        eligible_receivables = Decimal(data.get('receivables', '0'))
        eligible_financial_assets = Decimal(data.get('financial_assets', '0'))
        
        # Calculate deductible liabilities
        deductible_liabilities = Decimal(data.get('liabilities', '0'))
        
        # Get nisab threshold and zakat rate
        nisab_threshold = Decimal(data.get('nisab_threshold', settings.default_nisab_threshold if settings else '0'))
        zakat_rate = Decimal(data.get('zakat_rate', settings.default_zakat_rate if settings else '2.50'))
        
        # Calculate total eligible assets
        total_eligible = eligible_cash + eligible_inventory + eligible_receivables + eligible_financial_assets
        
        # Calculate net eligible assets
        net_eligible = total_eligible - deductible_liabilities
        
        # Calculate zakat amount
        if net_eligible >= nisab_threshold:
            zakat_amount = net_eligible * (zakat_rate / Decimal('100'))
        else:
            zakat_amount = Decimal('0.00')
        
        # Save calculation
        calculation = ZakatCalculation.objects.create(
            organization=self.organization,
            calculation_method=data.get('calculation_method', 'standard'),
            start_date=data.get('start_date', timezone.now().date()),
            end_date=data.get('end_date', timezone.now().date()),
            eligible_cash=eligible_cash,
            eligible_inventory=eligible_inventory,
            eligible_receivables=eligible_receivables,
            eligible_financial_assets=eligible_financial_assets,
            deductible_liabilities=deductible_liabilities,
            nisab_threshold=nisab_threshold,
            total_eligible_assets=total_eligible,
            net_eligible_assets=net_eligible,
            zakat_amount=zakat_amount,
            zakat_rate=zakat_rate,
            notes=data.get('notes', ''),
            calculated_by=self.user if self.user.is_authenticated else None
        )
        
        return {
            'id': str(calculation.id),
            'calculation_method': calculation.calculation_method,
            'start_date': calculation.start_date.isoformat(),
            'end_date': calculation.end_date.isoformat(),
            'eligible_cash': float(eligible_cash),
            'eligible_inventory': float(eligible_inventory),
            'eligible_receivables': float(eligible_receivables),
            'eligible_financial_assets': float(eligible_financial_assets),
            'total_eligible_assets': float(total_eligible),
            'deductible_liabilities': float(deductible_liabilities),
            'net_eligible_assets': float(net_eligible),
            'nisab_threshold': float(nisab_threshold),
            'zakat_rate': float(zakat_rate),
            'zakat_amount': float(zakat_amount),
            'nisab_met': net_eligible >= nisab_threshold,
            'created_at': calculation.created_at.isoformat(),
        }
    
    def get_zakat_settings(self):
        """
        Get zakat settings for the organization.
        """
        try:
            return ZakatSettings.objects.get(organization=self.organization)
        except ZakatSettings.DoesNotExist:
            return None
    
    def create_zakat_settings(self, data):
        """
        Create zakat settings for the organization.
        """
        settings = ZakatSettings.objects.create(
            organization=self.organization,
            default_nisab_threshold=Decimal(data.get('default_nisab_threshold', '0')),
            default_zakat_rate=Decimal(data.get('default_zakat_rate', '2.50')),
            default_calculation_method=data.get('default_calculation_method', 'standard'),
            include_cash=data.get('include_cash', True),
            include_inventory=data.get('include_inventory', True),
            include_receivables=data.get('include_receivables', True),
            include_financial_assets=data.get('include_financial_assets', True),
            deduct_payables=data.get('deduct_payables', True),
            deduct_loans=data.get('deduct_loans', True)
        )
        
        return self.get_zakat_settings_data(settings)
    
    def update_zakat_settings(self, pk, data):
        """
        Update zakat settings.
        """
        try:
            settings = ZakatSettings.objects.get(pk=pk, organization=self.organization)
            
            if 'default_nisab_threshold' in data:
                settings.default_nisab_threshold = Decimal(data['default_nisab_threshold'])
            if 'default_zakat_rate' in data:
                settings.default_zakat_rate = Decimal(data['default_zakat_rate'])
            if 'default_calculation_method' in data:
                settings.default_calculation_method = data['default_calculation_method']
            if 'include_cash' in data:
                settings.include_cash = data['include_cash']
            if 'include_inventory' in data:
                settings.include_inventory = data['include_inventory']
            if 'include_receivables' in data:
                settings.include_receivables = data['include_receivables']
            if 'include_financial_assets' in data:
                settings.include_financial_assets = data['include_financial_assets']
            if 'deduct_payables' in data:
                settings.deduct_payables = data['deduct_payables']
            if 'deduct_loans' in data:
                settings.deduct_loans = data['deduct_loans']
            
            settings.save()
            
            return self.get_zakat_settings_data(settings)
        except ZakatSettings.DoesNotExist:
            return None
    
    def record_zakat_payment(self, data):
        """
        Record a zakat payment.
        """
        payment = ZakatPayment.objects.create(
            organization=self.organization,
            calculation_id=data.get('calculation_id'),
            amount=Decimal(data.get('amount')),
            currency=data.get('currency', 'DZD'),
            payment_method=data.get('payment_method', 'cash'),
            payment_date=data.get('payment_date', timezone.now().date()),
            reference=data.get('reference', ''),
            recipient=data.get('recipient', ''),
            notes=data.get('notes', ''),
            recorded_by=self.user if self.user.is_authenticated else None
        )
        
        return self.get_zakat_payment_data(payment)
    
    def get_zakat_settings_data(self, settings):
        """
        Get zakat settings data for API responses.
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
    
    def get_zakat_payment_data(self, payment):
        """
        Get zakat payment data for API responses.
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
