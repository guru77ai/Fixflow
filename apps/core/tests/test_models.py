"""
Tests for Core models
"""
import pytest
from django.test import TestCase
from django.db import models
from apps.core.models import TimeStampedModel, UUIDModel, OrganizationAndBranchScopedModel
from apps.organizations.models import Organization
from apps.branches.models import Branch
import uuid


class TestTimeStampedModel(TestCase):
    """Test TimeStampedModel functionality"""
    
    def test_created_at_auto_now_add(self):
        """Test that created_at is set on creation"""
        from django.utils import timezone
        
        class TestModel(TimeStampedModel):
            name = models.CharField(max_length=100)
            
            class Meta:
                app_label = 'core'
        
        before_creation = timezone.now()
        obj = TestModel.objects.create(name='Test')
        after_creation = timezone.now()
        
        self.assertIsNotNone(obj.created_at)
        self.assertTrue(before_creation <= obj.created_at <= after_creation)
        self.assertIsNotNone(obj.updated_at)


class TestUUIDModel(TestCase):
    """Test UUIDModel functionality"""
    
    def test_uuid_field(self):
        """Test that uuid field is created and is a valid UUID"""
        class TestModel(UUIDModel):
            name = models.CharField(max_length=100)
            
            class Meta:
                app_label = 'core'
        
        obj = TestModel.objects.create(name='Test')
        self.assertTrue(hasattr(obj, 'uuid'))
        self.assertIsInstance(obj.uuid, uuid.UUID)


class TestOrganizationAndBranchScopedModel(TestCase):
    """Test OrganizationAndBranchScopedModel functionality"""
    
    def setUp(self):
        self.org = Organization.objects.create(name='Test Org', code='TO')
        self.branch = Branch.objects.create(
            name='Test Branch',
            code='TB',
            organization=self.org
        )
    
    def test_organization_field(self):
        """Test that organization field is created"""
        class TestModel(OrganizationAndBranchScopedModel):
            name = models.CharField(max_length=100)
            
            class Meta:
                app_label = 'core'
        
        obj = TestModel.objects.create(
            name='Test',
            organization=self.org,
            branch=self.branch
        )
        self.assertTrue(hasattr(obj, 'organization'))
        self.assertEqual(obj.organization, self.org)
    
    def test_branch_field(self):
        """Test that branch field is created"""
        class TestModel(OrganizationAndBranchScopedModel):
            name = models.CharField(max_length=100)
            
            class Meta:
                app_label = 'core'
        
        obj = TestModel.objects.create(
            name='Test',
            organization=self.org,
            branch=self.branch
        )
        self.assertTrue(hasattr(obj, 'branch'))
        self.assertEqual(obj.branch, self.branch)
