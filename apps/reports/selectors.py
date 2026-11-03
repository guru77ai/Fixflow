"""
Selectors for the reports application.
"""
from django.db.models import Count, Sum, Avg, F
from django.utils import timezone
from decimal import Decimal

# Optional imports for Phase 2+ apps (may not exist yet)
try:
    from apps.repairs.models import Repair
    HAS_REPAIRS = True
except ImportError:
    HAS_REPAIRS = False
    Repair = None

try:
    from apps.sales.models import Sale
    HAS_SALES = True
except ImportError:
    HAS_SALES = False
    Sale = None

try:
    from apps.products.models import Product
    HAS_PRODUCTS = True
except ImportError:
    HAS_PRODUCTS = False
    Product = None

try:
    from apps.inventory.models import StockMovement
    HAS_INVENTORY = True
except ImportError:
    HAS_INVENTORY = False
    StockMovement = None

try:
    from apps.payments.models import Payment
    HAS_PAYMENTS = True
except ImportError:
    HAS_PAYMENTS = False
    Payment = None

try:
    from apps.expenses.models import Expense
    HAS_EXPENSES = True
except ImportError:
    HAS_EXPENSES = False
    Expense = None


class ReportSelector:
    """
    Selector for report queries.
    """
    
    def __init__(self, request):
        self.request = request
        self.user = request.user
        self.organization = getattr(request, 'current_organization', None)
        self.branch = getattr(request, 'current_branch', None)
    
    def get_report_dashboard(self, **filters):
        """
        Get dashboard report data.
        """
        return {
            'stats': self.get_stats(),
            'charts': {
                'sales_by_day': self.get_sales_by_day(),
                'repairs_by_status': self.get_repairs_by_status(),
                'top_products': self.get_top_products(),
                'revenue_by_category': self.get_revenue_by_category(),
            },
            'recent_transactions': self.get_recent_transactions(),
        }
    
    def get_sales_report(self, **filters):
        """
        Get sales report data.
        """
        return {
            'summary': self.get_sales_summary(**filters),
            'by_day': self.get_sales_by_day(**filters),
            'by_product': self.get_sales_by_product(**filters),
            'by_customer': self.get_sales_by_customer(**filters),
            'by_payment_method': self.get_sales_by_payment_method(**filters),
        }
    
    def get_repair_report(self, **filters):
        """
        Get repair report data.
        """
        return {
            'summary': self.get_repair_summary(**filters),
            'by_status': self.get_repairs_by_status(**filters),
            'by_technician': self.get_repairs_by_technician(**filters),
            'by_device': self.get_repairs_by_device(**filters),
            'by_day': self.get_repairs_by_day(**filters),
        }
    
    def get_inventory_report(self, **filters):
        """
        Get inventory report data.
        """
        return {
            'summary': self.get_inventory_summary(**filters),
            'by_product': self.get_inventory_by_product(**filters),
            'low_stock': self.get_low_stock_products(**filters),
            'stock_movements': self.get_stock_movements(**filters),
        }
    
    def get_financial_report(self, **filters):
        """
        Get financial report data.
        """
        return {
            'summary': self.get_financial_summary(**filters),
            'income': self.get_income_report(**filters),
            'expenses': self.get_expenses_report(**filters),
            'profit_loss': self.get_profit_loss_report(**filters),
        }
    
    def get_stats(self):
        """
        Get summary statistics.
        """
        stats = {}
        
        # Sales stats
        if HAS_SALES:
            try:
                sales = Sale.objects.filter(organization=self.organization)
                if self.branch:
                    sales = sales.filter(branch=self.branch)
                
                stats['total_sales'] = sales.count()
                stats['total_revenue'] = float(sales.aggregate(total=Sum('total'))['total'] or 0)
                stats['today_sales'] = sales.filter(created_at__date=timezone.now().date()).count()
                stats['today_revenue'] = float(sales.filter(
                    created_at__date=timezone.now().date()
                ).aggregate(total=Sum('total'))['total'] or 0)
            except Exception:
                pass
        
        # Repair stats
        if HAS_REPAIRS:
            try:
                repairs = Repair.objects.filter(organization=self.organization)
                if self.branch:
                    repairs = repairs.filter(branch=self.branch)
                
                stats['total_repairs'] = repairs.count()
                stats['pending_repairs'] = repairs.filter(
                    status__in=['received', 'diagnosis', 'awaiting_approval', 'awaiting_parts', 'in_progress', 'testing']
                ).count()
                stats['completed_repairs'] = repairs.filter(status='delivered').count()
            except Exception:
                pass
        
        # Customer stats
        try:
            from apps.customers.models import Customer
            customers = Customer.objects.filter(organization=self.organization)
            if self.branch:
                customers = customers.filter(branch=self.branch)
            
            stats['total_customers'] = customers.count()
        except Exception:
            pass
        
        # Product stats
        if HAS_PRODUCTS:
            try:
                products = Product.objects.filter(organization=self.organization)
                stats['total_products'] = products.count()
            except Exception:
                pass
        
        return stats
    
    def get_sales_by_day(self, days=7):
        """
        Get sales grouped by day.
        """
        data = []
        
        if HAS_SALES:
            try:
                from django.db.models.functions import TruncDate
                
                sales = Sale.objects.filter(
                    organization=self.organization,
                    created_at__gte=timezone.now() - timezone.timedelta(days=days)
                )
                
                if self.branch:
                    sales = sales.filter(branch=self.branch)
                
                daily_sales = sales.annotate(
                    date=TruncDate('created_at')
                ).values('date').annotate(
                    count=Count('id'),
                    total=Sum('total')
                ).order_by('date')
                
                for item in daily_sales:
                    data.append({
                        'date': item['date'].isoformat(),
                        'count': item['count'],
                        'total': float(item['total'] or 0)
                    })
            except Exception:
                pass
        
        return data
    
    def get_repairs_by_status(self):
        """
        Get repairs grouped by status.
        """
        data = []
        
        if HAS_REPAIRS:
            try:
                repairs = Repair.objects.filter(organization=self.organization)
                if self.branch:
                    repairs = repairs.filter(branch=self.branch)
                
                status_counts = repairs.values('status').annotate(
                    count=Count('id')
                ).order_by('status')
                
                for item in status_counts:
                    data.append({
                        'status': item['status'],
                        'count': item['count']
                    })
            except Exception:
                pass
        
        return data
    
    def get_top_products(self, limit=5):
        """
        Get top selling products.
        """
        data = []
        
        if HAS_SALES and HAS_PRODUCTS:
            try:
                from apps.sales.models import SaleLine
                
                sale_lines = SaleLine.objects.filter(
                    sale__organization=self.organization
                )
                
                if self.branch:
                    sale_lines = sale_lines.filter(sale__branch=self.branch)
                
                product_sales = sale_lines.values('product__id', 'product__name').annotate(
                    quantity=Sum('quantity'),
                    total=Sum('total')
                ).order_by('-total')[:limit]
                
                for item in product_sales:
                    data.append({
                        'id': str(item['product__id']),
                        'name': item['product__name'],
                        'quantity': int(item['quantity'] or 0),
                        'total': float(item['total'] or 0)
                    })
            except Exception:
                pass
        
        return data
    
    def get_recent_transactions(self, limit=10):
        """
        Get recent transactions.
        """
        transactions = []
        
        # Get recent sales
        if HAS_SALES:
            try:
                sales = Sale.objects.filter(organization=self.organization)
                if self.branch:
                    sales = sales.filter(branch=self.branch)
                
                for sale in sales.order_by('-created_at')[:limit]:
                    transactions.append({
                        'type': 'sale',
                        'id': str(sale.id),
                        'number': sale.invoice_number,
                        'amount': float(sale.total),
                        'customer': sale.customer.get_full_name() if sale.customer else 'N/A',
                        'date': sale.created_at.isoformat(),
                    })
            except Exception:
                pass
        
        # Get recent repairs
        if HAS_REPAIRS:
            try:
                repairs = Repair.objects.filter(organization=self.organization)
                if self.branch:
                    repairs = repairs.filter(branch=self.branch)
                
                for repair in repairs.order_by('-created_at')[:limit]:
                    transactions.append({
                        'type': 'repair',
                        'id': str(repair.id),
                        'number': repair.repair_number,
                        'amount': float(repair.total),
                        'customer': repair.customer.get_full_name() if repair.customer else 'N/A',
                        'status': repair.status,
                        'date': repair.created_at.isoformat(),
                    })
            except Exception:
                pass
        
        # Sort by date and return
        transactions.sort(key=lambda x: x['date'], reverse=True)
        return transactions[:limit]
    
    def get_sales_summary(self, **filters):
        """
        Get sales summary.
        """
        summary = {}
        
        if HAS_SALES:
            try:
                sales = Sale.objects.filter(organization=self.organization)
                if self.branch:
                    sales = sales.filter(branch=self.branch)
                
                # Apply date filters
                if 'start_date' in filters:
                    sales = sales.filter(created_at__gte=filters['start_date'])
                if 'end_date' in filters:
                    sales = sales.filter(created_at__lte=filters['end_date'])
                
                summary['total_sales'] = sales.count()
                summary['total_revenue'] = float(sales.aggregate(total=Sum('total'))['total'] or 0)
                summary['total_tax'] = float(sales.aggregate(total=Sum('tax_amount'))['total'] or 0)
                summary['total_discount'] = float(sales.aggregate(total=Sum('discount_amount'))['total'] or 0)
                summary['average_sale'] = float(sales.aggregate(avg=Avg('total'))['avg'] or 0)
                summary['net_revenue'] = summary['total_revenue'] - summary['total_tax'] - summary['total_discount']
            except Exception:
                pass
        
        return summary
