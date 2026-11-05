"""
Services for CRM module
"""
from django.db import transaction
from django.utils import timezone
from .models import Customer, Device, CustomerCommunication, CustomerDocument


class CustomerService:
    """Service class for customer operations."""
    
    @staticmethod
    def create_customer(data, organization, branch, created_by=None):
        """Create a new customer."""
        from apps.accounts.models import User
        
        customer_data = {
            'organization': organization,
            'branch': branch,
            'code': data.get('code'),
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name', ''),
            'company_name': data.get('company_name'),
            'email': data.get('email'),
            'phone': data.get('phone'),
            'mobile': data.get('mobile'),
            'whatsapp': data.get('whatsapp'),
            'address_line_1': data.get('address_line_1'),
            'address_line_2': data.get('address_line_2'),
            'city': data.get('city'),
            'state': data.get('state'),
            'postal_code': data.get('postal_code'),
            'country': data.get('country', 'Algeria'),
            'gender': data.get('gender', 'unknown'),
            'date_of_birth': data.get('date_of_birth'),
            'tax_id': data.get('tax_id'),
            'status': data.get('status', 'active'),
            'customer_type_id': data.get('customer_type_id'),
            'customer_group_id': data.get('customer_group_id'),
            'source_id': data.get('source_id'),
            'notes': data.get('notes'),
            'facebook': data.get('facebook'),
            'twitter': data.get('twitter'),
            'instagram': data.get('instagram'),
            'referred_by_id': data.get('referred_by_id'),
            'referral_code': data.get('referral_code'),
            'credit_balance': data.get('credit_balance', 0),
            'loyalty_points': data.get('loyalty_points', 0),
        }
        
        customer = Customer.objects.create(**customer_data)
        
        # Log creation
        CustomerCommunication.objects.create(
            organization=organization,
            branch=branch,
            customer=customer,
            communication_type='other',
            direction='inbound',
            subject='Customer Created',
            message=f'Customer {customer.code} created by {created_by.get_full_name() if created_by else "System"}',
            status='closed'
        )
        
        return customer
    
    @staticmethod
    def update_customer(customer, data):
        """Update customer information."""
        for key, value in data.items():
            if hasattr(customer, key) and key != 'id':
                setattr(customer, key, value)
        customer.save()
        return customer
    
    @staticmethod
    def get_customer_by_phone(phone, organization=None):
        """Get customer by phone number."""
        queryset = Customer.objects.filter(phone=phone)
        if organization:
            queryset = queryset.filter(organization=organization)
        return queryset.first()
    
    @staticmethod
    def get_customer_by_email(email, organization=None):
        """Get customer by email."""
        queryset = Customer.objects.filter(email=email)
        if organization:
            queryset = queryset.filter(organization=organization)
        return queryset.first()
    
    @staticmethod
    def get_customer_by_code(code, organization=None):
        """Get customer by code."""
        queryset = Customer.objects.filter(code=code)
        if organization:
            queryset = queryset.filter(organization=organization)
        return queryset.first()
    
    @staticmethod
    def search_customers(query, organization, branch=None, limit=10):
        """Search customers by name, phone, or code."""
        from django.db.models import Q
        
        queryset = Customer.objects.filter(organization=organization)
        
        if branch:
            queryset = queryset.filter(branch=branch)
        
        if query:
            queryset = queryset.filter(
                Q(code__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(company_name__icontains=query) |
                Q(phone__icontains=query) |
                Q(mobile__icontains=query) |
                Q(email__icontains=query)
            )
        
        return queryset[:limit]
    
    @staticmethod
    def get_customer_statistics(customer):
        """Get statistics for a customer."""
        from django.db.models import Count, Sum
        from apps.repair.models import RepairOrder
        from apps.pos.models import Sale
        
        stats = {
            'total_repairs': RepairOrder.objects.filter(
                customer=customer
            ).count(),
            'total_sales': Sale.objects.filter(
                customer=customer
            ).count(),
            'total_spent': Sale.objects.filter(
                customer=customer
            ).aggregate(total=Sum('total_amount'))['total'] or 0,
            'devices_count': Device.objects.filter(
                customer=customer
            ).count(),
        }
        
        return stats


class DeviceService:
    """Service class for device operations."""
    
    @staticmethod
    def create_device(data, customer, organization, branch):
        """Create a new device for a customer."""
        device_data = {
            'organization': organization,
            'branch': branch,
            'customer': customer,
            'category_id': data.get('category_id'),
            'brand_id': data.get('brand_id'),
            'model_id': data.get('model_id'),
            'name': data.get('name'),
            'serial_number': data.get('serial_number'),
            'imei_1': data.get('imei_1'),
            'imei_2': data.get('imei_2'),
            'mac_address': data.get('mac_address'),
            'color': data.get('color'),
            'storage': data.get('storage'),
            'ram': data.get('ram'),
            'os_version': data.get('os_version'),
            'purchase_date': data.get('purchase_date'),
            'purchase_price': data.get('purchase_price'),
            'warranty_expiry': data.get('warranty_expiry'),
            'status': data.get('status', 'used'),
            'notes': data.get('notes'),
            'tag': data.get('tag'),
        }
        
        device = Device.objects.create(**device_data)
        return device
    
    @staticmethod
    def get_device_by_imei(imei, organization=None):
        """Get device by IMEI number."""
        from django.db.models import Q
        queryset = Device.objects.filter(Q(imei_1=imei) | Q(imei_2=imei))
        if organization:
            queryset = queryset.filter(organization=organization)
        return queryset.first()
    
    @staticmethod
    def get_device_by_serial(serial, organization=None):
        """Get device by serial number."""
        queryset = Device.objects.filter(serial_number=serial)
        if organization:
            queryset = queryset.filter(organization=organization)
        return queryset.first()
    
    @staticmethod
    def search_devices(query, organization, customer=None, limit=10):
        """Search devices by various criteria."""
        from django.db.models import Q
        
        queryset = Device.objects.filter(organization=organization)
        
        if customer:
            queryset = queryset.filter(customer=customer)
        
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(serial_number__icontains=query) |
                Q(imei_1__icontains=query) |
                Q(imei_2__icontains=query) |
                Q(mac_address__icontains=query) |
                Q(tag__icontains=query) |
                Q(model__name__icontains=query) |
                Q(brand__name__icontains=query)
            )
        
        return queryset[:limit]


class CommunicationService:
    """Service class for customer communications."""
    
    @staticmethod
    def create_communication(data, organization, branch, created_by=None):
        """Create a new communication record."""
        communication_data = {
            'organization': organization,
            'branch': branch,
            'customer_id': data.get('customer_id'),
            'communication_type': data.get('communication_type'),
            'direction': data.get('direction', 'inbound'),
            'subject': data.get('subject'),
            'message': data.get('message'),
            'response': data.get('response'),
            'related_to': data.get('related_to'),
            'status': data.get('status', 'open'),
            'follow_up_required': data.get('follow_up_required', False),
            'follow_up_date': data.get('follow_up_date'),
            'assigned_to_id': data.get('assigned_to_id'),
        }
        
        communication = CustomerCommunication.objects.create(**communication_data)
        return communication
    
    @staticmethod
    def get_open_communications(branch=None, assigned_to=None):
        """Get open communications that need follow-up."""
        from django.utils import timezone
        
        queryset = CustomerCommunication.objects.filter(
            status__in=['open', 'pending']
        )
        
        if branch:
            queryset = queryset.filter(branch=branch)
        
        if assigned_to:
            queryset = queryset.filter(assigned_to=assigned_to)
        
        # Filter by follow-up date
        queryset = queryset.filter(
            models.Q(follow_up_required=True) |
            models.Q(follow_up_date__lte=timezone.now())
        )
        
        return queryset.order_by('follow_up_date')


class DocumentService:
    """Service class for customer documents."""
    
    @staticmethod
    def create_document(data, organization, branch):
        """Create a new document record."""
        document_data = {
            'organization': organization,
            'branch': branch,
            'customer_id': data.get('customer_id'),
            'document_type': data.get('document_type'),
            'title': data.get('title'),
            'file': data.get('file'),
            'description': data.get('description'),
            'expiry_date': data.get('expiry_date'),
            'is_verified': data.get('is_verified', False),
        }
        
        document = CustomerDocument.objects.create(**document_data)
        return document
