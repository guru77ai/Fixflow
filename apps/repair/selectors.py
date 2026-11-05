"""
Selectors for Repair module
"""
from django.db.models import Q, Count, Sum, Avg
from django.utils import timezone
from .models import (
    RepairOrder, RepairPart, RepairService, RepairChecklist,
    RepairAttachment, RepairOrderHistory, RepairTemplate,
    RepairStatus, RepairPriority, RepairCategory, RepairType
)


class RepairOrderSelector:
    """Selector for repair order queries."""
    
    @staticmethod
    def get_all_orders(organization, branch=None, status=None, priority=None, 
                      technician=None, search=None, start_date=None, end_date=None,
                      ordering='-created_at'):
        """Get all repair orders with optional filters."""
        queryset = RepairOrder.objects.filter(organization=organization)
        
        if branch:
            queryset = queryset.filter(branch=branch)
        
        if status:
            queryset = queryset.filter(status=status)
        
        if priority:
            queryset = queryset.filter(priority=priority)
        
        if technician:
            queryset = queryset.filter(assigned_to=technician)
        
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        
        if search:
            queryset = queryset.filter(
                Q(order_number__icontains=search) |
                Q(customer__first_name__icontains=search) |
                Q(customer__last_name__icontains=search) |
                Q(customer__company_name__icontains=search) |
                Q(customer__phone__icontains=search) |
                Q(device__name__icontains=search) |
                Q(device_name__icontains=search) |
                Q(device_imei__icontains=search) |
                Q(device_serial__icontains=search) |
                Q(issue_description__icontains=search)
            )
        
        return queryset.order_by(ordering)
    
    @staticmethod
    def get_recent_orders(organization, branch=None, limit=10):
        """Get recent repair orders."""
        queryset = RepairOrder.objects.filter(organization=organization)
        if branch:
            queryset = queryset.filter(branch=branch)
        return queryset.order_by('-created_at')[:limit]
    
    @staticmethod
    def get_orders_by_customer(customer):
        """Get all repair orders for a customer."""
        return RepairOrder.objects.filter(customer=customer).order_by('-created_at')
    
    @staticmethod
    def get_orders_by_device(device):
        """Get all repair orders for a device."""
        return RepairOrder.objects.filter(
            Q(device=device) |
            Q(device_imei=device.imei_1) |
            Q(device_imei=device.imei_2) |
            Q(device_serial=device.serial_number)
        ).order_by('-created_at')
    
    @staticmethod
    def get_orders_by_status(status, organization, branch=None):
        """Get repair orders by status."""
        queryset = RepairOrder.objects.filter(
            organization=organization,
            status=status
        )
        if branch:
            queryset = queryset.filter(branch=branch)
        return queryset.order_by('-created_at')
    
    @staticmethod
    def get_orders_by_priority(priority, organization, branch=None):
        """Get repair orders by priority."""
        queryset = RepairOrder.objects.filter(
            organization=organization,
            priority=priority
        )
        if branch:
            queryset = queryset.filter(branch=branch)
        return queryset.order_by('-created_at')
    
    @staticmethod
    def get_overdue_orders(organization, branch=None):
        """Get overdue repair orders."""
        queryset = RepairOrder.objects.filter(
            organization=organization,
            promised_date__lt=timezone.now(),
            status__code__in=['received', 'diagnosed', 'in_progress']
        )
        if branch:
            queryset = queryset.filter(branch=branch)
        return queryset.order_by('promised_date')
    
    @staticmethod
    def get_orders_by_technician(technician, organization, branch=None, status=None):
        """Get repair orders assigned to a technician."""
        queryset = RepairOrder.objects.filter(
            organization=organization,
            assigned_to=technician
        )
        if branch:
            queryset = queryset.filter(branch=branch)
        if status:
            queryset = queryset.filter(status=status)
        return queryset.order_by('-created_at')
    
    @staticmethod
    def get_unassigned_orders(organization, branch=None):
        """Get repair orders without a technician assigned."""
        queryset = RepairOrder.objects.filter(
            organization=organization,
            assigned_to__isnull=True
        )
        if branch:
            queryset = queryset.filter(branch=branch)
        return queryset.order_by('-created_at')
    
    @staticmethod
    def get_urgent_orders(organization, branch=None):
        """Get urgent repair orders."""
        queryset = RepairOrder.objects.filter(
            organization=organization,
            is_urgent=True
        )
        if branch:
            queryset = queryset.filter(branch=branch)
        return queryset.order_by('-created_at')
    
    @staticmethod
    def get_warranty_claims(organization, branch=None):
        """Get warranty repair orders."""
        queryset = RepairOrder.objects.filter(
            organization=organization,
            is_warranty_claim=True
        )
        if branch:
            queryset = queryset.filter(branch=branch)
        return queryset.order_by('-created_at')
    
    @staticmethod
    def get_orders_with_balance(organization, branch=None):
        """Get repair orders with outstanding balance."""
        queryset = RepairOrder.objects.filter(
            organization=organization,
            balance__gt=0
        )
        if branch:
            queryset = queryset.filter(branch=branch)
        return queryset.order_by('-created_at')
    
    @staticmethod
    def get_statistics(organization, branch=None):
        """Get repair order statistics."""
        queryset = RepairOrder.objects.filter(organization=organization)
        if branch:
            queryset = queryset.filter(branch=branch)
        
        stats = {
            'total': queryset.count(),
            'completed': queryset.filter(status__code='completed').count(),
            'in_progress': queryset.filter(status__code='in_progress').count(),
            'pending': queryset.filter(status__code__in=['received', 'diagnosed']).count(),
            'delivered': queryset.filter(status__code='delivered').count(),
            'cancelled': queryset.filter(status__code='cancelled').count(),
            'overdue': queryset.filter(
                promised_date__lt=timezone.now(),
                status__code__in=['received', 'diagnosed', 'in_progress']
            ).count(),
            'unassigned': queryset.filter(assigned_to__isnull=True).count(),
            'urgent': queryset.filter(is_urgent=True).count(),
            'warranty_claims': queryset.filter(is_warranty_claim=True).count(),
            'total_revenue': queryset.aggregate(total=Sum('final_amount'))['total'] or 0,
            'total_outstanding': queryset.aggregate(total=Sum('balance'))['total'] or 0,
            'avg_completion_time': queryset.filter(
                completed_date__isnull=False,
                started_date__isnull=False
            ).aggregate(
                avg=Avg('completed_date') - Avg('started_date')
            )['avg'] or 0,
        }
        
        return stats


class RepairPartSelector:
    """Selector for repair part queries."""
    
    @staticmethod
    def get_all_parts(repair_order=None, organization=None):
        """Get all repair parts with optional filters."""
        queryset = RepairPart.objects.all()
        if repair_order:
            queryset = queryset.filter(repair_order=repair_order)
        if organization:
            queryset = queryset.filter(repair_order__organization=organization)
        return queryset.order_by('-created_at')
    
    @staticmethod
    def get_parts_by_repair_order(repair_order):
        """Get all parts for a repair order."""
        return RepairPart.objects.filter(repair_order=repair_order).order_by('-created_at')
    
    @staticmethod
    def get_parts_by_product(product, organization=None):
        """Get all repair parts by product."""
        queryset = RepairPart.objects.filter(part=product)
        if organization:
            queryset = queryset.filter(repair_order__organization=organization)
        return queryset.order_by('-created_at')


class RepairServiceSelector:
    """Selector for repair service queries."""
    
    @staticmethod
    def get_all_services(repair_order=None, organization=None):
        """Get all repair services with optional filters."""
        queryset = RepairService.objects.all()
        if repair_order:
            queryset = queryset.filter(repair_order=repair_order)
        if organization:
            queryset = queryset.filter(repair_order__organization=organization)
        return queryset.order_by('-created_at')
    
    @staticmethod
    def get_services_by_repair_order(repair_order):
        """Get all services for a repair order."""
        return RepairService.objects.filter(repair_order=repair_order).order_by('-created_at')
    
    @staticmethod
    def get_services_by_technician(technician, organization=None):
        """Get all services performed by a technician."""
        queryset = RepairService.objects.filter(technician=technician)
        if organization:
            queryset = queryset.filter(repair_order__organization=organization)
        return queryset.order_by('-created_at')


class RepairChecklistSelector:
    """Selector for repair checklist queries."""
    
    @staticmethod
    def get_all_checklists(repair_order=None, organization=None):
        """Get all checklist items with optional filters."""
        queryset = RepairChecklist.objects.all()
        if repair_order:
            queryset = queryset.filter(repair_order=repair_order)
        if organization:
            queryset = queryset.filter(repair_order__organization=organization)
        return queryset.order_by('sequence')
    
    @staticmethod
    def get_checklists_by_repair_order(repair_order):
        """Get all checklist items for a repair order."""
        return RepairChecklist.objects.filter(repair_order=repair_order).order_by('sequence')
    
    @staticmethod
    def get_incomplete_checklists(repair_order):
        """Get incomplete checklist items for a repair order."""
        return RepairChecklist.objects.filter(
            repair_order=repair_order,
            is_completed=False
        ).order_by('sequence')


class RepairAttachmentSelector:
    """Selector for repair attachment queries."""
    
    @staticmethod
    def get_all_attachments(repair_order=None, organization=None):
        """Get all attachments with optional filters."""
        queryset = RepairAttachment.objects.all()
        if repair_order:
            queryset = queryset.filter(repair_order=repair_order)
        if organization:
            queryset = queryset.filter(repair_order__organization=organization)
        return queryset.order_by('-created_at')
    
    @staticmethod
    def get_attachments_by_repair_order(repair_order):
        """Get all attachments for a repair order."""
        return RepairAttachment.objects.filter(repair_order=repair_order).order_by('-created_at')


class RepairHistorySelector:
    """Selector for repair history queries."""
    
    @staticmethod
    def get_all_history(repair_order=None, organization=None):
        """Get all history records with optional filters."""
        queryset = RepairOrderHistory.objects.all()
        if repair_order:
            queryset = queryset.filter(repair_order=repair_order)
        if organization:
            queryset = queryset.filter(repair_order__organization=organization)
        return queryset.order_by('-created_at')
    
    @staticmethod
    def get_history_by_repair_order(repair_order):
        """Get all history for a repair order."""
        return RepairOrderHistory.objects.filter(repair_order=repair_order).order_by('-created_at')


class RepairTemplateSelector:
    """Selector for repair template queries."""
    
    @staticmethod
    def get_all_templates(organization, branch=None, active_only=True):
        """Get all repair templates."""
        queryset = RepairTemplate.objects.filter(organization=organization)
        if branch:
            queryset = queryset.filter(branch=branch)
        if active_only:
            queryset = queryset.filter(is_active=True)
        return queryset.order_by('name')
    
    @staticmethod
    def get_template_by_code(code, organization):
        """Get a template by code."""
        return RepairTemplate.objects.filter(
            code=code,
            organization=organization
        ).first()


class RepairStatusSelector:
    """Selector for repair status queries."""
    
    @staticmethod
    def get_all_statuses(initial_only=False, final_only=False):
        """Get all repair statuses."""
        queryset = RepairStatus.objects.all()
        if initial_only:
            queryset = queryset.filter(is_initial=True)
        if final_only:
            queryset = queryset.filter(is_final=True)
        return queryset.order_by('sequence')
    
    @staticmethod
    def get_status_by_code(code):
        """Get a status by code."""
        return RepairStatus.objects.filter(code=code).first()


class RepairPrioritySelector:
    """Selector for repair priority queries."""
    
    @staticmethod
    def get_all_priorities():
        """Get all repair priorities."""
        return RepairPriority.objects.all().order_by('-level')
    
    @staticmethod
    def get_priority_by_code(code):
        """Get a priority by code."""
        return RepairPriority.objects.filter(code=code).first()


class RepairCategorySelector:
    """Selector for repair category queries."""
    
    @staticmethod
    def get_all_categories(parent=None, active_only=True):
        """Get all repair categories."""
        queryset = RepairCategory.objects.all()
        if parent:
            queryset = queryset.filter(parent=parent)
        if active_only:
            queryset = queryset.filter(is_active=True)
        return queryset.order_by('name')
    
    @staticmethod
    def get_category_by_code(code):
        """Get a category by code."""
        return RepairCategory.objects.filter(code=code).first()
    
    @staticmethod
    def get_root_categories(active_only=True):
        """Get root categories (no parent)."""
        queryset = RepairCategory.objects.filter(parent__isnull=True)
        if active_only:
            queryset = queryset.filter(is_active=True)
        return queryset.order_by('name')


class RepairTypeSelector:
    """Selector for repair type queries."""
    
    @staticmethod
    def get_all_types(category=None, active_only=True):
        """Get all repair types."""
        queryset = RepairType.objects.all()
        if category:
            queryset = queryset.filter(category=category)
        if active_only:
            queryset = queryset.filter(is_active=True)
        return queryset.order_by('name')
    
    @staticmethod
    def get_type_by_code(code):
        """Get a repair type by code."""
        return RepairType.objects.filter(code=code).first()
