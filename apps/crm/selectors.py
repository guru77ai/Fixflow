"""
Selectors for CRM module
"""
from django.db.models import Q, Count, Sum, Avg
from .models import (
    Customer, Device, CustomerType, CustomerSource, 
    CustomerGroup, DeviceBrand, DeviceModel, DeviceCategory,
    CustomerCommunication, CustomerDocument
)


class CustomerSelector:
    """Selector for customer queries."""
    
    @staticmethod
    def get_all_customers(organization, branch=None, status=None, search=None, ordering='-created_at'):
        """Get all customers with optional filters."""
        queryset = Customer.objects.filter(organization=organization)
        
        if branch:
            queryset = queryset.filter(branch=branch)
        
        if status:
            queryset = queryset.filter(status=status)
        
        if search:
            queryset = queryset.filter(
                Q(code__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(company_name__icontains=search) |
                Q(phone__icontains=search) |
                Q(mobile__icontains=search) |
                Q(email__icontains=search)
            )
        
        return queryset.order_by(ordering)
    
    @staticmethod
    def get_active_customers(organization, branch=None):
        """Get all active customers."""
        return Customer.objects.filter(
            organization=organization,
            status='active'
        ).order_by('first_name', 'last_name')
    
    @staticmethod
    def get_customers_by_group(group):
        """Get all customers in a specific group."""
        return Customer.objects.filter(customer_group=group).order_by('first_name')
    
    @staticmethod
    def get_customers_by_type(customer_type):
        """Get all customers of a specific type."""
        return Customer.objects.filter(customer_type=customer_type).order_by('first_name')
    
    @staticmethod
    def get_vip_customers(organization):
        """Get all VIP customers."""
        return Customer.objects.filter(
            organization=organization,
            status='vip'
        ).order_by('-total_purchases')
    
    @staticmethod
    def get_customers_with_credit(organization):
        """Get customers with outstanding credit."""
        return Customer.objects.filter(
            organization=organization,
            credit_balance__gt=0
        ).order_by('-credit_balance')
    
    @staticmethod
    def get_customers_with_loyalty_points(organization):
        """Get customers with loyalty points."""
        return Customer.objects.filter(
            organization=organization,
            loyalty_points__gt=0
        ).order_by('-loyalty_points')
    
    @staticmethod
    def get_customer_statistics(organization):
        """Get overall customer statistics."""
        from django.db.models import Count
        
        stats = {
            'total': Customer.objects.filter(organization=organization).count(),
            'active': Customer.objects.filter(organization=organization, status='active').count(),
            'inactive': Customer.objects.filter(organization=organization, status='inactive').count(),
            'blocked': Customer.objects.filter(organization=organization, status='blocked').count(),
            'vip': Customer.objects.filter(organization=organization, status='vip').count(),
            'prospect': Customer.objects.filter(organization=organization, status='prospect').count(),
            'with_credit': Customer.objects.filter(organization=organization, credit_balance__gt=0).count(),
            'total_credit': Customer.objects.filter(
                organization=organization,
                credit_balance__gt=0
            ).aggregate(total=Sum('credit_balance'))['total'] or 0,
            'total_purchases': Customer.objects.filter(
                organization=organization
            ).aggregate(total=Sum('total_purchases'))['total'] or 0,
        }
        
        return stats


class DeviceSelector:
    """Selector for device queries."""
    
    @staticmethod
    def get_all_devices(organization, branch=None, customer=None, status=None, search=None):
        """Get all devices with optional filters."""
        queryset = Device.objects.filter(organization=organization)
        
        if branch:
            queryset = queryset.filter(branch=branch)
        
        if customer:
            queryset = queryset.filter(customer=customer)
        
        if status:
            queryset = queryset.filter(status=status)
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(serial_number__icontains=search) |
                Q(imei_1__icontains=search) |
                Q(imei_2__icontains=search) |
                Q(mac_address__icontains=search) |
                Q(tag__icontains=search) |
                Q(model__name__icontains=search) |
                Q(brand__name__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    @staticmethod
    def get_devices_by_customer(customer):
        """Get all devices for a specific customer."""
        return Device.objects.filter(customer=customer).order_by('-created_at')
    
    @staticmethod
    def get_devices_by_brand(brand, organization):
        """Get all devices of a specific brand."""
        return Device.objects.filter(
            brand=brand,
            organization=organization
        ).order_by('-created_at')
    
    @staticmethod
    def get_devices_by_category(category, organization):
        """Get all devices of a specific category."""
        return Device.objects.filter(
            category=category,
            organization=organization
        ).order_by('-created_at')
    
    @staticmethod
    def get_device_statistics(organization):
        """Get device statistics."""
        stats = {
            'total': Device.objects.filter(organization=organization).count(),
            'by_status': Device.objects.filter(
                organization=organization
            ).values('status').annotate(count=Count('id')),
            'by_category': Device.objects.filter(
                organization=organization
            ).values('category__name').annotate(count=Count('id')),
            'by_brand': Device.objects.filter(
                organization=organization
            ).values('brand__name').annotate(count=Count('id')),
        }
        
        return stats


class CustomerTypeSelector:
    """Selector for customer type queries."""
    
    @staticmethod
    def get_all_types(active_only=True):
        """Get all customer types."""
        queryset = CustomerType.objects.all()
        if active_only:
            queryset = queryset.filter(is_active=True)
        return queryset.order_by('name')
    
    @staticmethod
    def get_type_by_code(code):
        """Get customer type by code."""
        return CustomerType.objects.filter(code=code).first()


class CustomerSourceSelector:
    """Selector for customer source queries."""
    
    @staticmethod
    def get_all_sources(active_only=True):
        """Get all customer sources."""
        queryset = CustomerSource.objects.all()
        if active_only:
            queryset = queryset.filter(is_active=True)
        return queryset.order_by('name')
    
    @staticmethod
    def get_source_by_code(code):
        """Get customer source by code."""
        return CustomerSource.objects.filter(code=code).first()


class CustomerGroupSelector:
    """Selector for customer group queries."""
    
    @staticmethod
    def get_all_groups(organization, active_only=True):
        """Get all customer groups for an organization."""
        queryset = CustomerGroup.objects.filter(organization=organization)
        if active_only:
            queryset = queryset.filter(is_active=True)
        return queryset.order_by('name')
    
    @staticmethod
    def get_group_by_code(code, organization):
        """Get customer group by code."""
        return CustomerGroup.objects.filter(
            code=code,
            organization=organization
        ).first()


class DeviceBrandSelector:
    """Selector for device brand queries."""
    
    @staticmethod
    def get_all_brands(active_only=True):
        """Get all device brands."""
        queryset = DeviceBrand.objects.all()
        if active_only:
            queryset = queryset.filter(is_active=True)
        return queryset.order_by('name')
    
    @staticmethod
    def get_brand_by_code(code):
        """Get device brand by code."""
        return DeviceBrand.objects.filter(code=code).first()


class DeviceModelSelector:
    """Selector for device model queries."""
    
    @staticmethod
    def get_all_models(brand=None, active_only=True):
        """Get all device models."""
        queryset = DeviceModel.objects.all()
        if brand:
            queryset = queryset.filter(brand=brand)
        if active_only:
            queryset = queryset.filter(is_active=True)
        return queryset.order_by('brand__name', 'name')
    
    @staticmethod
    def get_model_by_code(code):
        """Get device model by code."""
        return DeviceModel.objects.filter(code=code).first()


class DeviceCategorySelector:
    """Selector for device category queries."""
    
    @staticmethod
    def get_all_categories(active_only=True):
        """Get all device categories."""
        queryset = DeviceCategory.objects.all()
        if active_only:
            queryset = queryset.filter(is_active=True)
        return queryset.order_by('name')
    
    @staticmethod
    def get_category_by_code(code):
        """Get device category by code."""
        return DeviceCategory.objects.filter(code=code).first()


class CommunicationSelector:
    """Selector for communication queries."""
    
    @staticmethod
    def get_all_communications(organization, branch=None, customer=None, status=None, search=None):
        """Get all communications with optional filters."""
        queryset = CustomerCommunication.objects.filter(organization=organization)
        
        if branch:
            queryset = queryset.filter(branch=branch)
        
        if customer:
            queryset = queryset.filter(customer=customer)
        
        if status:
            queryset = queryset.filter(status=status)
        
        if search:
            queryset = queryset.filter(
                Q(subject__icontains=search) |
                Q(message__icontains=search) |
                Q(customer__first_name__icontains=search) |
                Q(customer__last_name__icontains=search) |
                Q(related_to__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    @staticmethod
    def get_communications_by_customer(customer):
        """Get all communications for a specific customer."""
        return CustomerCommunication.objects.filter(customer=customer).order_by('-created_at')
    
    @staticmethod
    def get_open_communications(organization):
        """Get all open communications."""
        return CustomerCommunication.objects.filter(
            organization=organization,
            status__in=['open', 'pending']
        ).order_by('-created_at')


class DocumentSelector:
    """Selector for document queries."""
    
    @staticmethod
    def get_all_documents(organization, branch=None, customer=None, document_type=None):
        """Get all documents with optional filters."""
        queryset = CustomerDocument.objects.filter(organization=organization)
        
        if branch:
            queryset = queryset.filter(branch=branch)
        
        if customer:
            queryset = queryset.filter(customer=customer)
        
        if document_type:
            queryset = queryset.filter(document_type=document_type)
        
        return queryset.order_by('-created_at')
    
    @staticmethod
    def get_documents_by_customer(customer):
        """Get all documents for a specific customer."""
        return CustomerDocument.objects.filter(customer=customer).order_by('-created_at')
    
    @staticmethod
    def get_expiring_documents(organization, days=30):
        """Get documents that are expiring soon."""
        from django.utils import timezone
        from datetime import timedelta
        
        expiry_threshold = timezone.now() + timedelta(days=days)
        
        return CustomerDocument.objects.filter(
            organization=organization,
            expiry_date__lte=expiry_threshold,
            expiry_date__gte=timezone.now()
        ).order_by('expiry_date')
