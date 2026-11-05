"""
Signals for POS module
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Sale


@receiver(post_save, sender=Sale)
def update_customer_purchases(sender, instance, created, **kwargs):
    """Update customer's total purchases when a sale is created."""
    if created and instance.customer:
        customer = instance.customer
        customer.total_purchases += instance.total_amount
        customer.save(update_fields=['total_purchases'])
