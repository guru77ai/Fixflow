"""
Tests for Repair models
"""
import pytest
from django.test import TestCase
from apps.repair.models import (
    RepairStatus, RepairPriority, RepairCategory, RepairType,
    RepairOrder, RepairOrderHistory, RepairPart, RepairService,
    RepairChecklist, RepairAttachment, RepairTemplate
)


class TestRepairStatus(TestCase):
    """Test RepairStatus model"""
    
    def test_repair_status_creation(self):
        """Test creating a repair status"""
        status = RepairStatus.objects.create(
            name='Received',
            code='RCV',
            description='Device received',
            sequence=1,
            is_default=True,
            is_final=False,
            is_active=True
        )
        self.assertEqual(status.name, 'Received')
        self.assertEqual(status.code, 'RCV')
        self.assertTrue(status.is_default)
    
    def test_repair_status_str(self):
        """Test string representation of repair status"""
        status = RepairStatus.objects.create(
            name='In Progress',
            code='INP'
        )
        self.assertEqual(str(status), 'In Progress')


class TestRepairPriority(TestCase):
    """Test RepairPriority model"""
    
    def test_repair_priority_creation(self):
        """Test creating a repair priority"""
        priority = RepairPriority.objects.create(
            name='High',
            code='HIGH',
            level=1,
            sequence=1,
            color='#ff0000',
            is_active=True
        )
        self.assertEqual(priority.name, 'High')
        self.assertEqual(priority.level, 1)


class TestRepairCategory(TestCase):
    """Test RepairCategory model"""
    
    def test_repair_category_creation(self):
        """Test creating a repair category"""
        category = RepairCategory.objects.create(
            name='Hardware',
            code='HW',
            description='Hardware repairs',
            sequence=1,
            is_active=True
        )
        self.assertEqual(category.name, 'Hardware')


class TestRepairType(TestCase):
    """Test RepairType model"""
    
    def test_repair_type_creation(self):
        """Test creating a repair type"""
        category = RepairCategory.objects.create(name='Hardware', code='HW')
        repair_type = RepairType.objects.create(
            name='Screen Replacement',
            code='SCR',
            category=category,
            estimated_duration=30,
            base_price=100.00,
            description='Replace broken screen',
            is_active=True
        )
        self.assertEqual(repair_type.name, 'Screen Replacement')
        self.assertEqual(repair_type.category.name, 'Hardware')


class TestRepairOrder(TestCase):
    """Test RepairOrder model"""
    
    def test_repair_order_creation(self):
        """Test creating a repair order"""
        from apps.crm.models import Customer, Device
        from apps.core.models import Organization, Branch
        
        # Create organization and branch
        org = Organization.objects.create(name='Test Org', code='TO')
        branch = Branch.objects.create(name='Test Branch', code='TB', organization=org)
        
        # Create customer
        customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            organization=org,
            branch=branch
        )
        
        # Create device
        device = Device.objects.create(
            name='My Phone',
            device_type='Smartphone',
            customer=customer,
            organization=org,
            branch=branch
        )
        
        # Create repair order
        status = RepairStatus.objects.create(name='Received', code='RCV', is_default=True)
        priority = RepairPriority.objects.create(name='High', code='HIGH', level=1)
        category = RepairCategory.objects.create(name='Hardware', code='HW')
        repair_type = RepairType.objects.create(name='Screen Replacement', code='SCR', category=category)
        
        repair_order = RepairOrder.objects.create(
            customer=customer,
            device=device,
            status=status,
            priority=priority,
            category=category,
            type=repair_type,
            issue='Broken screen',
            received_date='2023-01-01',
            organization=org,
            branch=branch
        )
        self.assertEqual(repair_order.issue, 'Broken screen')
        self.assertEqual(repair_order.customer.full_name, 'John Doe')


class TestRepairPart(TestCase):
    """Test RepairPart model"""
    
    def test_repair_part_creation(self):
        """Test creating a repair part"""
        part = RepairPart.objects.create(
            name='Screen',
            part_number='SCR001',
            category='Display',
            quantity=10,
            unit_cost=50.00,
            total_cost=500.00,
            description='LCD Screen for Samsung Galaxy'
        )
        self.assertEqual(part.name, 'Screen')
        self.assertEqual(part.part_number, 'SCR001')


class TestRepairService(TestCase):
    """Test RepairService model"""
    
    def test_repair_service_creation(self):
        """Test creating a repair service"""
        category = RepairCategory.objects.create(name='Hardware', code='HW')
        service = RepairService.objects.create(
            name='Diagnostic',
            code='DIAG',
            category=category,
            duration=15,
            price=25.00,
            description='Device diagnostic service',
            is_active=True
        )
        self.assertEqual(service.name, 'Diagnostic')
        self.assertEqual(service.price, 25.00)
