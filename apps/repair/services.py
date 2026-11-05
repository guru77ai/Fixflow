"""
Services for Repair module
"""
from django.db import transaction
from django.utils import timezone
from decimal import Decimal
from .models import (
    RepairOrder, RepairPart, RepairService, RepairChecklist,
    RepairAttachment, RepairOrderHistory, RepairTemplate
)


class RepairOrderService:
    """Service class for repair order operations."""
    
    @staticmethod
    @transaction.atomic
    def create_repair_order(data, organization, branch, created_by=None):
        """Create a new repair order."""
        from apps.crm.models import Customer, Device
        from .models import RepairStatus, RepairPriority
        
        # Get default status
        default_status = RepairStatus.objects.filter(is_initial=True).first()
        if not default_status:
            default_status = RepairStatus.objects.first()
        
        # Get default priority
        default_priority = RepairPriority.objects.first()
        
        # Get customer
        customer = None
        if data.get('customer_id'):
            customer = Customer.objects.get(id=data['customer_id'], organization=organization)
        
        # Get device
        device = None
        if data.get('device_id'):
            device = Device.objects.get(id=data['device_id'], organization=organization)
        
        # Generate order number
        order_number = data.get('order_number')
        if not order_number:
            order_number = RepairOrderService.generate_order_number(organization, branch)
        
        repair_order_data = {
            'organization': organization,
            'branch': branch,
            'order_number': order_number,
            'order_type': data.get('order_type', 'standard'),
            'customer': customer,
            'device': device,
            'device_name': data.get('device_name'),
            'device_imei': data.get('device_imei'),
            'device_serial': data.get('device_serial'),
            'device_brand_id': data.get('device_brand_id'),
            'device_model_id': data.get('device_model_id'),
            'repair_type_id': data.get('repair_type_id'),
            'repair_category_id': data.get('repair_category_id'),
            'status': default_status,
            'priority_id': data.get('priority_id', default_priority.id if default_priority else None),
            'issue_description': data.get('issue_description'),
            'reported_issue': data.get('reported_issue'),
            'diagnosis': data.get('diagnosis'),
            'assigned_to_id': data.get('assigned_to_id'),
            'promised_date': data.get('promised_date'),
            'quotation_amount': Decimal(data.get('quotation_amount', 0) or 0),
            'labor_cost': Decimal(data.get('labor_cost', 0) or 0),
            'parts_cost': Decimal(data.get('parts_cost', 0) or 0),
            'total_cost': Decimal(data.get('total_cost', 0) or 0),
            'discount': Decimal(data.get('discount', 0) or 0),
            'tax_amount': Decimal(data.get('tax_amount', 0) or 0),
            'final_amount': Decimal(data.get('final_amount', 0) or 0),
            'amount_paid': Decimal(data.get('amount_paid', 0) or 0),
            'balance': Decimal(data.get('balance', 0) or 0),
            'payment_method': data.get('payment_method'),
            'payment_status': data.get('payment_status', 'pending'),
            'warranty_type': data.get('warranty_type', 'none'),
            'warranty_period': data.get('warranty_period', 0),
            'warranty_expiry': data.get('warranty_expiry'),
            'internal_notes': data.get('internal_notes'),
            'customer_notes': data.get('customer_notes'),
            'is_urgent': data.get('is_urgent', False),
            'is_warranty_claim': data.get('is_warranty_claim', False),
            'is_approved': data.get('is_approved', False),
            'approval_date': data.get('approval_date'),
            'approved_by_id': data.get('approved_by_id'),
            'status_changed_by': created_by,
            'tags': data.get('tags'),
        }
        
        repair_order = RepairOrder.objects.create(**repair_order_data)
        
        # Create initial history
        RepairOrderHistory.objects.create(
            repair_order=repair_order,
            changed_by=created_by,
            change_type='status_change',
            field_name='status',
            old_value=None,
            new_value=str(default_status),
            comments='Repair order created'
        )
        
        return repair_order
    
    @staticmethod
    def generate_order_number(organization, branch):
        """Generate a unique order number."""
        from django.utils import timezone
        
        # Format: ORG-BRANCH-YYYYMMDD-XXXX
        org_code = organization.code if organization else 'ORG'
        branch_code = branch.code if branch else 'BR'
        date_str = timezone.now().strftime('%Y%m%d')
        
        # Get last order number for today
        last_order = RepairOrder.objects.filter(
            order_number__startswith=f"{org_code}-{branch_code}-{date_str}"
        ).order_by('-order_number').first()
        
        if last_order:
            # Extract the sequence number
            last_seq = last_order.order_number.split('-')[-1]
            try:
                seq = int(last_seq) + 1
            except ValueError:
                seq = 1
        else:
            seq = 1
        
        return f"{org_code}-{branch_code}-{date_str}-{seq:04d}"
    
    @staticmethod
    @transaction.atomic
    def update_status(repair_order, new_status, changed_by=None, comments=None):
        """Update repair order status and track history."""
        old_status = repair_order.status
        repair_order.status = new_status
        repair_order.status_changed_at = timezone.now()
        repair_order.status_changed_by = changed_by
        repair_order.save()
        
        # Create history record
        RepairOrderHistory.objects.create(
            repair_order=repair_order,
            changed_by=changed_by,
            change_type='status_change',
            field_name='status',
            old_value=str(old_status),
            new_value=str(new_status),
            comments=comments or f'Status changed from {old_status} to {new_status}'
        )
        
        # Update timestamps based on status
        if new_status.code == 'in_progress':
            repair_order.started_date = timezone.now()
        elif new_status.code == 'completed':
            repair_order.completed_date = timezone.now()
        elif new_status.code == 'delivered':
            repair_order.delivered_date = timezone.now()
        
        repair_order.save()
        
        return repair_order
    
    @staticmethod
    @transaction.atomic
    def assign_technician(repair_order, technician, assigned_by=None):
        """Assign a technician to a repair order."""
        old_technician = repair_order.assigned_to
        repair_order.assigned_to = technician
        repair_order.save()
        
        # Create history record
        RepairOrderHistory.objects.create(
            repair_order=repair_order,
            changed_by=assigned_by,
            change_type='assignment',
            field_name='assigned_to',
            old_value=str(old_technician) if old_technician else None,
            new_value=str(technician) if technician else None,
            comments=f'Assigned to {technician}'
        )
        
        return repair_order
    
    @staticmethod
    def calculate_totals(repair_order):
        """Calculate and update totals for a repair order."""
        from django.db.models import Sum
        
        # Calculate parts cost
        parts_total = RepairPart.objects.filter(
            repair_order=repair_order
        ).aggregate(total=Sum('total_cost'))['total'] or 0
        
        # Calculate services cost
        services_total = RepairService.objects.filter(
            repair_order=repair_order
        ).aggregate(total=Sum('total_price'))['total'] or 0
        
        # Update repair order
        repair_order.parts_cost = parts_total
        repair_order.labor_cost = services_total
        repair_order.total_cost = parts_total + services_total
        
        # Calculate final amount
        final_amount = repair_order.total_cost - repair_order.discount + repair_order.tax_amount
        repair_order.final_amount = final_amount
        repair_order.balance = final_amount - repair_order.amount_paid
        
        repair_order.save()
        
        return repair_order
    
    @staticmethod
    def get_repair_orders_by_status(status, organization, branch=None):
        """Get repair orders by status."""
        queryset = RepairOrder.objects.filter(
            organization=organization,
            status=status
        )
        if branch:
            queryset = queryset.filter(branch=branch)
        return queryset.order_by('-created_at')
    
    @staticmethod
    def get_overdue_repairs(organization, branch=None):
        """Get overdue repair orders."""
        from django.utils import timezone
        
        queryset = RepairOrder.objects.filter(
            organization=organization,
            promised_date__lt=timezone.now(),
            status__code__in=['received', 'diagnosed', 'in_progress']
        )
        if branch:
            queryset = queryset.filter(branch=branch)
        return queryset.order_by('promised_date')
    
    @staticmethod
    def get_repairs_by_technician(technician, organization, status=None):
        """Get repair orders assigned to a technician."""
        queryset = RepairOrder.objects.filter(
            organization=organization,
            assigned_to=technician
        )
        if status:
            queryset = queryset.filter(status=status)
        return queryset.order_by('-created_at')
    
    @staticmethod
    def get_repairs_by_customer(customer):
        """Get all repair orders for a customer."""
        return RepairOrder.objects.filter(
            customer=customer
        ).order_by('-created_at')
    
    @staticmethod
    def get_repairs_by_device(device):
        """Get all repair orders for a device."""
        return RepairOrder.objects.filter(
            models.Q(device=device) |
            models.Q(device_imei=device.imei_1) |
            models.Q(device_imei=device.imei_2) |
            models.Q(device_serial=device.serial_number)
        ).order_by('-created_at')


class RepairPartService:
    """Service class for repair part operations."""
    
    @staticmethod
    def add_part(repair_order, data, created_by=None):
        """Add a part to a repair order."""
        from apps.inventory.models import Product
        
        part = None
        if data.get('part_id'):
            part = Product.objects.get(id=data['part_id'])
        
        repair_part = RepairPart.objects.create(
            repair_order=repair_order,
            part=part,
            part_name=data.get('part_name'),
            part_code=data.get('part_code'),
            quantity=data.get('quantity', 1),
            unit_cost=data.get('unit_cost', 0),
            serial_number=data.get('serial_number'),
            is_warranty=data.get('is_warranty', False),
            notes=data.get('notes')
        )
        
        # Recalculate totals
        RepairOrderService.calculate_totals(repair_order)
        
        # Create history
        RepairOrderHistory.objects.create(
            repair_order=repair_order,
            changed_by=created_by,
            change_type='cost_update',
            field_name='parts',
            old_value=None,
            new_value=f"Added {repair_part.part_name} ({repair_part.quantity})",
            comments=f"Part added: {repair_part.part_name}"
        )
        
        return repair_part
    
    @staticmethod
    def remove_part(repair_part, removed_by=None):
        """Remove a part from a repair order."""
        repair_order = repair_part.repair_order
        part_name = repair_part.part_name
        
        repair_part.delete()
        
        # Recalculate totals
        RepairOrderService.calculate_totals(repair_order)
        
        # Create history
        RepairOrderHistory.objects.create(
            repair_order=repair_order,
            changed_by=removed_by,
            change_type='cost_update',
            field_name='parts',
            old_value=part_name,
            new_value=None,
            comments=f"Part removed: {part_name}"
        )
        
        return True


class RepairServiceService:
    """Service class for repair service operations."""
    
    @staticmethod
    def add_service(repair_order, data, created_by=None):
        """Add a service to a repair order."""
        from apps.inventory.models import Service
        
        service = None
        if data.get('service_id'):
            service = Service.objects.get(id=data['service_id'])
        
        repair_service = RepairService.objects.create(
            repair_order=repair_order,
            service=service,
            service_name=data.get('service_name'),
            service_code=data.get('service_code'),
            quantity=data.get('quantity', 1),
            unit_price=data.get('unit_price', 0),
            duration_minutes=data.get('duration_minutes', 0),
            technician_id=data.get('technician_id'),
            notes=data.get('notes')
        )
        
        # Recalculate totals
        RepairOrderService.calculate_totals(repair_order)
        
        # Create history
        RepairOrderHistory.objects.create(
            repair_order=repair_order,
            changed_by=created_by,
            change_type='cost_update',
            field_name='services',
            old_value=None,
            new_value=f"Added {repair_service.service_name}",
            comments=f"Service added: {repair_service.service_name}"
        )
        
        return repair_service
    
    @staticmethod
    def remove_service(repair_service, removed_by=None):
        """Remove a service from a repair order."""
        repair_order = repair_service.repair_order
        service_name = repair_service.service_name
        
        repair_service.delete()
        
        # Recalculate totals
        RepairOrderService.calculate_totals(repair_order)
        
        # Create history
        RepairOrderHistory.objects.create(
            repair_order=repair_order,
            changed_by=removed_by,
            change_type='cost_update',
            field_name='services',
            old_value=service_name,
            new_value=None,
            comments=f"Service removed: {service_name}"
        )
        
        return True


class RepairChecklistService:
    """Service class for repair checklist operations."""
    
    @staticmethod
    def add_checklist_item(repair_order, data, created_by=None):
        """Add a checklist item to a repair order."""
        checklist_item = RepairChecklist.objects.create(
            repair_order=repair_order,
            item=data.get('item'),
            description=data.get('description'),
            sequence=data.get('sequence', 0)
        )
        return checklist_item
    
    @staticmethod
    def complete_checklist_item(checklist_item, completed_by=None):
        """Mark a checklist item as completed."""
        checklist_item.is_completed = True
        checklist_item.completed_at = timezone.now()
        checklist_item.completed_by = completed_by
        checklist_item.save()
        return checklist_item
    
    @staticmethod
    def get_checklist_progress(repair_order):
        """Get checklist completion progress."""
        total = RepairChecklist.objects.filter(repair_order=repair_order).count()
        completed = RepairChecklist.objects.filter(
            repair_order=repair_order,
            is_completed=True
        ).count()
        
        if total > 0:
            percentage = (completed / total) * 100
        else:
            percentage = 0
        
        return {
            'total': total,
            'completed': completed,
            'percentage': percentage,
            'incomplete': total - completed
        }


class RepairAttachmentService:
    """Service class for repair attachment operations."""
    
    @staticmethod
    def add_attachment(repair_order, file, data, created_by=None):
        """Add an attachment to a repair order."""
        attachment = RepairAttachment.objects.create(
            repair_order=repair_order,
            file=file,
            file_type=data.get('file_type', 'photo'),
            title=data.get('title'),
            description=data.get('description'),
            uploaded_by=created_by
        )
        return attachment
    
    @staticmethod
    def remove_attachment(attachment, removed_by=None):
        """Remove an attachment from a repair order."""
        attachment.delete()
        return True


class RepairTemplateService:
    """Service class for repair template operations."""
    
    @staticmethod
    def create_template(data, organization, branch):
        """Create a new repair template."""
        template = RepairTemplate.objects.create(
            organization=organization,
            branch=branch,
            name=data.get('name'),
            code=data.get('code'),
            description=data.get('description'),
            repair_type_id=data.get('repair_type_id'),
            estimated_cost=data.get('estimated_cost', 0),
            estimated_duration=data.get('estimated_duration', 60),
            checklist_items=data.get('checklist_items'),
            default_parts=data.get('default_parts'),
            default_services=data.get('default_services'),
            is_active=data.get('is_active', True)
        )
        return template
    
    @staticmethod
    def apply_template(template, repair_order_data, organization, branch, created_by=None):
        """Create a repair order from a template."""
        # Merge template data with repair order data
        data = {
            **repair_order_data,
            'repair_type_id': template.repair_type_id,
            'estimated_cost': template.estimated_cost,
        }
        
        # Create repair order
        repair_order = RepairOrderService.create_repair_order(
            data=data,
            organization=organization,
            branch=branch,
            created_by=created_by
        )
        
        # Add checklist items from template
        if template.checklist_items:
            for item in template.checklist_items:
                RepairChecklistService.add_checklist_item(
                    repair_order,
                    {'item': item.get('item'), 'description': item.get('description')},
                    created_by
                )
        
        # Add default parts from template
        if template.default_parts:
            for part in template.default_parts:
                RepairPartService.add_part(
                    repair_order,
                    {
                        'part_name': part.get('name'),
                        'quantity': part.get('quantity', 1),
                        'unit_cost': part.get('cost', 0)
                    },
                    created_by
                )
        
        # Add default services from template
        if template.default_services:
            for service in template.default_services:
                RepairServiceService.add_service(
                    repair_order,
                    {
                        'service_name': service.get('name'),
                        'quantity': service.get('quantity', 1),
                        'unit_price': service.get('price', 0)
                    },
                    created_by
                )
        
        return repair_order


class RepairStatisticsService:
    """Service class for repair statistics."""
    
    @staticmethod
    def get_statistics(organization, branch=None, start_date=None, end_date=None):
        """Get repair statistics."""
        from django.db.models import Count, Sum, Avg
        from django.utils import timezone
        
        queryset = RepairOrder.objects.filter(organization=organization)
        
        if branch:
            queryset = queryset.filter(branch=branch)
        
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        
        stats = {
            'total': queryset.count(),
            'completed': queryset.filter(status__code='completed').count(),
            'in_progress': queryset.filter(status__code='in_progress').count(),
            'pending': queryset.filter(status__code__in=['received', 'diagnosed']).count(),
            'overdue': queryset.filter(
                promised_date__lt=timezone.now(),
                status__code__in=['received', 'diagnosed', 'in_progress']
            ).count(),
            'by_status': list(queryset.values('status__name').annotate(count=Count('id'))),
            'by_priority': list(queryset.values('priority__name').annotate(count=Count('id'))),
            'by_type': list(queryset.values('order_type').annotate(count=Count('id'))),
            'total_revenue': queryset.aggregate(total=Sum('final_amount'))['total'] or 0,
            'avg_repair_time': queryset.filter(
                completed_date__isnull=False,
                started_date__isnull=False
            ).aggregate(avg=Avg('completed_date') - Avg('started_date'))['avg'] or 0,
            'avg_cost': queryset.aggregate(avg=Avg('final_amount'))['avg'] or 0,
        }
        
        return stats
