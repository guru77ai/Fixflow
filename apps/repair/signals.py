"""
Signals for Repair module
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import RepairOrder


@receiver(post_save, sender=RepairOrder)
def update_customer_repair_count(sender, instance, created, **kwargs):
    """Update customer's total repairs count when a repair order is created."""
    if created:
        customer = instance.customer
        if customer:
            customer.total_repairs += 1
            customer.save(update_fields=['total_repairs'])
