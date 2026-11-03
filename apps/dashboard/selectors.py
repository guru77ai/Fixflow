"""
Selectors for the dashboard application.
"""
from django.utils import timezone
from django.db.models import Count, Sum, Q
from decimal import Decimal
from apps.audit_logs.models import AuditLog


class DashboardSelector:
    """
    Selector for dashboard data.
    """
    
    def __init__(self, request):
        self.request = request
        self.user = request.user
        self.organization = getattr(request, 'current_organization', None)
        self.branch = getattr(request, 'current_branch', None)
    
    def get_stats(self):
        """
        Get dashboard statistics.
        """
        stats = {
            'total_repairs': 0,
            'pending_repairs': 0,
            'completed_repairs': 0,
            'total_customers': 0,
            'total_products': 0,
            'total_sales': Decimal('0.00'),
            'total_purchases': Decimal('0.00'),
            'today_sales': Decimal('0.00'),
            'today_repairs': 0,
        }
        
        # Get repair statistics
        try:
            from apps.repairs.models import Repair
            
            repairs = Repair.objects.filter(
                organization=self.organization
            )
            
            if self.branch:
                repairs = repairs.filter(branch=self.branch)
            
            stats['total_repairs'] = repairs.count()
            stats['pending_repairs'] = repairs.filter(
                status__in=['received', 'diagnosis', 'awaiting_approval', 'awaiting_parts', 'in_progress', 'testing']
            ).count()
            stats['completed_repairs'] = repairs.filter(status='delivered').count()
            
            # Today's repairs
            today = timezone.now().date()
            stats['today_repairs'] = repairs.filter(
                created_at__date=today
            ).count()
        except Exception:
            pass
        
        # Get customer statistics
        try:
            from apps.customers.models import Customer
            
            customers = Customer.objects.filter(organization=self.organization)
            
            if self.branch:
                customers = customers.filter(branch=self.branch)
            
            stats['total_customers'] = customers.count()
        except Exception:
            pass
        
        # Get product statistics
        try:
            from apps.products.models import Product
            
            products = Product.objects.filter(organization=self.organization)
            stats['total_products'] = products.count()
        except Exception:
            pass
        
        return stats
    
    def get_recent_activity(self, limit=10):
        """
        Get recent activity from audit logs.
        """
        activity = []
        
        try:
            logs = AuditLog.objects.filter(
                organization=self.organization
            )
            
            if self.branch:
                logs = logs.filter(branch=self.branch)
            
            logs = logs.order_by('-created_at')[:limit]
            
            for log in logs:
                activity.append({
                    'id': str(log.id),
                    'action': log.get_action_display(),
                    'entity_type': log.entity_type,
                    'entity_id': str(log.entity_id) if log.entity_id else None,
                    'entity_repr': log.entity_repr,
                    'user': log.user.get_short_name() if log.user else 'System',
                    'timestamp': log.created_at.isoformat(),
                    'timestamp_display': self.format_timestamp(log.created_at),
                })
        except Exception:
            pass
        
        return activity
    
    def get_chart_data(self):
        """
        Get chart data for the dashboard.
        """
        charts = {
            'repairs_by_status': self.get_repairs_by_status(),
            'sales_by_day': self.get_sales_by_day(),
            'top_products': self.get_top_products(),
        }
        return charts
    
    def get_repairs_by_status(self):
        """
        Get repairs grouped by status.
        """
        data = []
        
        try:
            from apps.repairs.models import Repair
            
            repairs = Repair.objects.filter(
                organization=self.organization
            )
            
            if self.branch:
                repairs = repairs.filter(branch=self.branch)
            
            # Get status distribution
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
    
    def get_sales_by_day(self, days=7):
        """
        Get sales data for the last N days.
        """
        data = []
        
        try:
            from apps.sales.models import Sale
            from django.db.models.functions import TruncDate
            
            sales = Sale.objects.filter(
                organization=self.organization,
                created_at__gte=timezone.now() - timezone.timedelta(days=days)
            )
            
            if self.branch:
                sales = sales.filter(branch=self.branch)
            
            # Group by day
            daily_sales = sales.annotate(
                date=TruncDate('created_at')
            ).values('date').annotate(
                total=Sum('total')
            ).order_by('date')
            
            for item in daily_sales:
                data.append({
                    'date': item['date'].isoformat(),
                    'date_display': self.format_date(item['date']),
                    'total': float(item['total'] or 0)
                })
        except Exception:
            pass
        
        return data
    
    def get_top_products(self, limit=5):
        """
        Get top selling products.
        """
        data = []
        
        try:
            from apps.sales.models import SaleLine
            from apps.products.models import Product
            
            sale_lines = SaleLine.objects.filter(
                sale__organization=self.organization
            )
            
            if self.branch:
                sale_lines = sale_lines.filter(sale__branch=self.branch)
            
            # Group by product
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
    
    def format_timestamp(self, timestamp):
        """
        Format a timestamp for display.
        """
        from django.utils import timezone
        from django.utils.translation import gettext_lazy as _
        
        now = timezone.now()
        diff = now - timestamp
        
        if diff.days == 0:
            if diff.seconds < 60:
                return _("Just now")
            elif diff.seconds < 3600:
                minutes = diff.seconds // 60
                return _("{count} minute ago").format(count=minutes) if minutes == 1 else _("{count} minutes ago").format(count=minutes)
            else:
                hours = diff.seconds // 3600
                return _("{count} hour ago").format(count=hours) if hours == 1 else _("{count} hours ago").format(count=hours)
        elif diff.days == 1:
            return _("Yesterday")
        elif diff.days < 7:
            return _("{count} days ago").format(count=diff.days)
        else:
            return timestamp.strftime('%Y-%m-%d %H:%M')
    
    def format_date(self, date):
        """
        Format a date for display.
        """
        return date.strftime('%Y-%m-%d')
