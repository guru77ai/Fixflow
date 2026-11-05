"""
Services for POS module
"""
from django.db import transaction
from django.utils import timezone
from decimal import Decimal
from .models import Sale, SaleItem, SalePayment, Receipt, Refund, RefundItem, CashRegister, POSSession


class SaleService:
    """Service class for sale operations."""
    
    @staticmethod
    @transaction.atomic
    def create_sale(data, organization, branch, created_by=None):
        """Create a new sale."""
        from apps.crm.models import Customer
        from apps.inventory.models import Product, Service
        
        # Generate sale number
        sale_number = data.get('sale_number')
        if not sale_number:
            sale_number = SaleService.generate_sale_number(organization, branch)
        
        customer = None
        if data.get('customer_id'):
            customer = Customer.objects.get(id=data['customer_id'], organization=organization)
        
        cash_register = None
        if data.get('cash_register_id'):
            cash_register = CashRegister.objects.get(id=data['cash_register_id'], organization=organization)
        
        sale_data = {
            'organization': organization,
            'branch': branch,
            'sale_number': sale_number,
            'sale_type': data.get('sale_type', 'retail'),
            'status': data.get('status', 'draft'),
            'customer': customer,
            'cash_register': cash_register,
            'subtotal': Decimal(data.get('subtotal', 0) or 0),
            'discount': Decimal(data.get('discount', 0) or 0),
            'tax_amount': Decimal(data.get('tax_amount', 0) or 0),
            'total_amount': Decimal(data.get('total_amount', 0) or 0),
            'amount_paid': Decimal(data.get('amount_paid', 0) or 0),
            'balance': Decimal(data.get('balance', 0) or 0),
            'payment_method_id': data.get('payment_method_id'),
            'payment_reference': data.get('payment_reference'),
            'payment_status': data.get('payment_status', 'pending'),
            'is_credit': data.get('is_credit', False),
            'credit_days': data.get('credit_days', 0),
            'due_date': data.get('due_date'),
            'is_invoice': data.get('is_invoice', False),
            'invoice_number': data.get('invoice_number'),
            'sold_by': created_by,
            'notes': data.get('notes'),
        }
        
        sale = Sale.objects.create(**sale_data)
        
        # Create receipt
        Receipt.objects.create(
            organization=organization,
            branch=branch,
            sale=sale,
            receipt_number=SaleService.generate_receipt_number(organization, branch, sale_number),
            receipt_type=data.get('receipt_type', 'thermal')
        )
        
        return sale
    
    @staticmethod
    def generate_sale_number(organization, branch):
        """Generate a unique sale number."""
        from django.utils import timezone
        
        org_code = organization.code if organization else 'ORG'
        branch_code = branch.code if branch else 'BR'
        date_str = timezone.now().strftime('%Y%m%d')
        
        last_sale = Sale.objects.filter(
            sale_number__startswith=f"{org_code}-{branch_code}-{date_str}"
        ).order_by('-sale_number').first()
        
        if last_sale:
            last_seq = last_sale.sale_number.split('-')[-1]
            try:
                seq = int(last_seq) + 1
            except ValueError:
                seq = 1
        else:
            seq = 1
        
        return f"{org_code}-{branch_code}-{date_str}-{seq:04d}"
    
    @staticmethod
    def generate_receipt_number(organization, branch, sale_number):
        """Generate a unique receipt number."""
        return f"R-{sale_number}"
    
    @staticmethod
    def add_item(sale, data, created_by=None):
        """Add an item to a sale."""
        from apps.inventory.models import Product, Service
        
        product = None
        service = None
        
        if data.get('product_id'):
            product = Product.objects.get(id=data['product_id'])
        elif data.get('service_id'):
            service = Service.objects.get(id=data['service_id'])
        
        sale_item = SaleItem.objects.create(
            sale=sale,
            product=product,
            service=service,
            product_name=data.get('product_name'),
            product_code=data.get('product_code'),
            quantity=Decimal(data.get('quantity', 1) or 1),
            unit_price=Decimal(data.get('unit_price', 0) or 0),
            discount=Decimal(data.get('discount', 0) or 0),
            tax_rate=Decimal(data.get('tax_rate', 0) or 0),
            serial_number=data.get('serial_number'),
            notes=data.get('notes')
        )
        
        # Recalculate sale totals
        SaleService.calculate_totals(sale)
        
        return sale_item
    
    @staticmethod
    def calculate_totals(sale):
        """Calculate and update sale totals."""
        from django.db.models import Sum
        
        items_total = sale.items.aggregate(total=Sum('total_price'))['total'] or 0
        items_discount = sale.items.aggregate(total=Sum('discount'))['total'] or 0
        items_tax = sale.items.aggregate(total=Sum('tax_amount'))['total'] or 0
        
        sale.subtotal = items_total
        sale.tax_amount = items_tax
        sale.total_amount = items_total - sale.discount + items_tax
        sale.balance = sale.total_amount - sale.amount_paid
        sale.save()
        
        return sale
    
    @staticmethod
    def add_payment(sale, data, created_by=None):
        """Add a payment to a sale."""
        payment = SalePayment.objects.create(
            sale=sale,
            payment_method_id=data.get('payment_method_id'),
            amount=Decimal(data.get('amount', 0) or 0),
            reference=data.get('reference'),
            transaction_id=data.get('transaction_id'),
            status=data.get('status', 'completed'),
            processed_by=created_by,
            notes=data.get('notes')
        )
        
        # Update sale payment status
        SaleService.update_payment_status(sale)
        
        return payment
    
    @staticmethod
    def update_payment_status(sale):
        """Update sale payment status based on payments."""
        from django.db.models import Sum
        
        total_paid = sale.payments.aggregate(total=Sum('amount'))['total'] or 0
        sale.amount_paid = total_paid
        sale.balance = sale.total_amount - total_paid
        
        if sale.balance <= 0:
            sale.payment_status = 'paid'
        elif sale.amount_paid > 0:
            sale.payment_status = 'partial'
        else:
            sale.payment_status = 'pending'
        
        sale.save()
        
        return sale
    
    @staticmethod
    def get_sales_by_date(organization, branch=None, start_date=None, end_date=None):
        """Get sales by date range."""
        queryset = Sale.objects.filter(organization=organization)
        
        if branch:
            queryset = queryset.filter(branch=branch)
        
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        
        return queryset.order_by('-created_at')
    
    @staticmethod
    def get_sales_by_customer(customer):
        """Get all sales for a customer."""
        return Sale.objects.filter(customer=customer).order_by('-created_at')
    
    @staticmethod
    def get_sales_by_status(status, organization, branch=None):
        """Get sales by status."""
        queryset = Sale.objects.filter(
            organization=organization,
            status=status
        )
        if branch:
            queryset = queryset.filter(branch=branch)
        return queryset.order_by('-created_at')


class CashRegisterService:
    """Service class for cash register operations."""
    
    @staticmethod
    def open_register(cash_register, initial_amount, opened_by):
        """Open a cash register."""
        cash_register.is_open = True
        cash_register.opened_at = timezone.now()
        cash_register.opened_by = opened_by
        cash_register.initial_amount = initial_amount
        cash_register.current_amount = initial_amount
        cash_register.save()
        
        return cash_register
    
    @staticmethod
    def close_register(cash_register, closed_by):
        """Close a cash register."""
        cash_register.is_open = False
        cash_register.closed_at = timezone.now()
        cash_register.closed_by = closed_by
        cash_register.save()
        
        return cash_register
    
    @staticmethod
    def get_open_registers(organization, branch=None):
        """Get all open cash registers."""
        queryset = CashRegister.objects.filter(
            organization=organization,
            is_open=True
        )
        if branch:
            queryset = queryset.filter(branch=branch)
        return queryset


class POSSessionService:
    """Service class for POS session operations."""
    
    @staticmethod
    def create_session(user, cash_register, initial_amount):
        """Create a new POS session."""
        session = POSSession.objects.create(
            organization=cash_register.organization,
            branch=cash_register.branch,
            user=user,
            cash_register=cash_register,
            session_key=str(uuid.uuid4()),
            initial_amount=initial_amount,
            final_amount=initial_amount
        )
        
        return session
    
    @staticmethod
    def end_session(session, final_amount):
        """End a POS session."""
        session.ended_at = timezone.now()
        session.final_amount = final_amount
        session.is_active = False
        session.save()
        
        return session
