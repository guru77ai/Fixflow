"""
Tests for Core models
"""
from django.db import models
from django.test import TestCase
from apps.core.models import TimeStampedModel, UUIDModel, OrganizationAndBranchScopedModel


class TestTimeStampedModel(TestCase):
    """Test TimeStampedModel functionality"""

    def test_created_at_auto_now_add(self):
        """Test that created_at and updated_at are present on the model."""
        class TestModel(TimeStampedModel):
            name = models.CharField(max_length=100)

            class Meta:
                app_label = 'core'

        self.assertTrue(hasattr(TestModel, 'created_at'))
        self.assertTrue(hasattr(TestModel, 'updated_at'))
        self.assertEqual(TestModel._meta.get_field('created_at').auto_now_add, True)
        self.assertEqual(TestModel._meta.get_field('updated_at').auto_now, True)


class TestUUIDModel(TestCase):
    """Test UUIDModel functionality"""

    def test_uuid_field(self):
        """Test that uuid field is created"""
        field = UUIDModel._meta.get_field('id')
        self.assertEqual(field.primary_key, True)
        self.assertEqual(field.unique, True)
        self.assertTrue(hasattr(field, 'default'))


class TestOrganizationAndBranchScopedModel(TestCase):
    """Test OrganizationAndBranchScopedModel functionality"""

    def test_organization_field(self):
        """Test that organization field is created"""
        field = OrganizationAndBranchScopedModel._meta.get_field('organization')
        self.assertEqual(field.name, 'organization')

    def test_branch_field(self):
        """Test that branch field is created"""
        field = OrganizationAndBranchScopedModel._meta.get_field('branch')
        self.assertEqual(field.name, 'branch')
