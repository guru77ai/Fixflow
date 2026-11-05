"""Services for Financial module"""
from django.db import transaction
from decimal import Decimal
from .models import Invoice, InvoiceItem, InvoicePayment, Payment, Expense


class InvoiceService:
    @staticmethod
    @transaction.atomic
    def create_invoice(data, organization, branch, created_by=None):
        from apps.crm.models import Customer
        from apps.suppliers.models import Supplier
        
        invoice_type = data.get('invoice_type_id')
        status = data.get('status_id')
        customer = Customer.objects.get(id=data['customer_id']) if data.get('customer_id') else None
        supplier = Supplier.objects.get(id=data['supplier_id']) if data.get('supplier_id') else None
        
        invoice = Invoice.objects.create(
            organization=organization,
            branch=branch,
            invoice_number=InvoiceService.generate_invoice_number(organization, branch),
            invoice_type_id=invoice_type,
            status_id=status,
            customer=customer,
            supplier=supplier,
            reference=data.get('reference'),
            reference_type=data.get('reference_type'),
            subtotal=Decimal(data.get('subtotal', 0) or 0),
            discount=Decimal(data.get('discount', 0) or 0),
            tax_amount=Decimal(data.get('tax_amount', 0) or 0),
            total_amount=Decimal(data.get('total_amount', 0) or 0),
            amount_paid=Decimal(data.get('amount_paid', 0) or 0),
            balance=Decimal(data.get('balance', 0) or 0),
            payment_status=data.get('payment_status', 'pending'),
            due_date=data.get('due_date'),
            paid_date=data.get('paid_date'),
            payment_method_id=data.get('payment_method_id'),
            payment_reference=data.get('payment_reference'),
            is_recurring=data.get('is_recurring', False),
            recurring_frequency=data.get('recurring_frequency'),
            recurring_end_date=data.get('recurring_end_date'),
            terms=data.get('terms'),
            created_by=created_by,
            approved_by_id=data.get('approved_by_id'),
            notes=data.get('notes'),
        )
        return invoice
    
    @staticmethod
    def generate_invoice_number(organization, branch):
        from django.utils import timezone
        org_code = organization.code if organization else 'ORG'
        branch_code = branch.code if branch else 'BR'
        date_str = timezone.now().strftime('%Y%m%d')
        last_inv = Invoice.objects.filter(invoice_number__startswith=f"{org_code}-{branch_code}-{date_str}").order_by('-invoice_number').first()
        seq = 1
        if last_inv:
            try:
                seq = int(last_inv.invoice_number.split('-')[-1]) + 1
            except:
                seq = 1
        return f"{org_code}-{branch_code}-{date_str}-{seq:04d}"


class ExpenseService:
    @staticmethod
    @transaction.atomic
    def create_expense(data, organization, branch, created_by=None):
        expense = Expense.objects.create(
            organization=organization,
            branch=branch,
            expense_number=ExpenseService.generate_expense_number(organization, branch),
            category_id=data.get('category_id'),
            status=data.get('status', 'draft'),
            title=data.get('title'),
            description=data.get('description'),
            amount=Decimal(data.get('amount', 0) or 0),
            tax_amount=Decimal(data.get('tax_amount', 0) or 0),
            total_amount=Decimal(data.get('total_amount', 0) or 0),
            payment_method_id=data.get('payment_method_id'),
            payment_reference=data.get('payment_reference'),
            expense_date=data.get('expense_date'),
            paid_date=data.get('paid_date'),
            supplier_id=data.get('supplier_id'),
            submitted_by=created_by,
            approved_by_id=data.get('approved_by_id'),
            paid_by_id=data.get('paid_by_id'),
            receipt_attached=data.get('receipt_attached', False),
            notes=data.get('notes'),
        )
        return expense
    
    @staticmethod
    def generate_expense_number(organization, branch):
        from django.utils import timezone
        org_code = organization.code if organization else 'ORG'
        branch_code = branch.code if branch else 'BR'
        date_str = timezone.now().strftime('%Y%m%d')
        last_exp = Expense.objects.filter(expense_number__startswith=f"{org_code}-{branch_code}-{date_str}").order_by('-expense_number').first()
        seq = 1
        if last_exp:
            try:
                seq = int(last_exp.expense_number.split('-')[-1]) + 1
            except:
                seq = 1
        return f"{org_code}-{branch_code}-{date_str}-{seq:04d}"


class PaymentService:
    @staticmethod
    @transaction.atomic
    def create_payment(data, organization, branch, created_by=None):
        payment = Payment.objects.create(
            organization=organization,
            branch=branch,
            payment_number=PaymentService.generate_payment_number(organization, branch),
            payment_type=data.get('payment_type', 'customer'),
            amount=Decimal(data.get('amount', 0) or 0),
            currency=data.get('currency', 'DZD'),
            payment_method_id=data.get('payment_method_id'),
            reference=data.get('reference'),
            customer_id=data.get('customer_id'),
            supplier_id=data.get('supplier_id'),
            related_to=data.get('related_to'),
            related_id=data.get('related_id'),
            status=data.get('status', 'completed'),
            processed_by=created_by,
            approved_by_id=data.get('approved_by_id'),
            notes=data.get('notes'),
        )
        return payment
    
    @staticmethod
    def generate_payment_number(organization, branch):
        from django.utils import timezone
        org_code = organization.code if organization else 'ORG'
        branch_code = branch.code if branch else 'BR'
        date_str = timezone.now().strftime('%Y%m%d')
        last_pay = Payment.objects.filter(payment_number__startswith=f"{org_code}-{branch_code}-{date_str}").order_by('-payment_number').first()
        seq = 1
        if last_pay:
            try:
                seq = int(last_pay.payment_number.split('-')[-1]) + 1
            except:
                seq = 1
        return f"{org_code}-{branch_code}-{date_str}-{seq:04d}"
