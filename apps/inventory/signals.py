"""
Signals for Inventory module
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import StockMovement


@receiver(post_save, sender=StockMovement)
def update_stock_after_movement(sender, instance, created, **kwargs):
    """Update product stock after a stock movement."""
    if created:
        product = instance.product
        if product:
            # Update current stock
            if instance.movement_type == 'in':
                product.current_stock += instance.quantity
            elif instance.movement_type == 'out':
                product.current_stock -= instance.quantity
            
            product.save(update_fields=['current_stock'])
