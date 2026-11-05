"""
API URLs for Repair module
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    RepairStatusViewSet, RepairPriorityViewSet, RepairCategoryViewSet,
    RepairTypeViewSet, RepairOrderViewSet, RepairOrderHistoryViewSet,
    RepairPartViewSet, RepairServiceViewSet, RepairChecklistViewSet,
    RepairAttachmentViewSet, RepairTemplateViewSet
)

router = DefaultRouter()

# Status, Priority, Category, Type
router.register(r'repair-statuses', RepairStatusViewSet, basename='repairstatus')
router.register(r'repair-priorities', RepairPriorityViewSet, basename='repairpriority')
router.register(r'repair-categories', RepairCategoryViewSet, basename='repaircategory')
router.register(r'repair-types', RepairTypeViewSet, basename='repairtype')

# Main entities
router.register(r'repair-orders', RepairOrderViewSet, basename='repairorder')
router.register(r'repair-history', RepairOrderHistoryViewSet, basename='repairhistory')
router.register(r'repair-parts', RepairPartViewSet, basename='repairpart')
router.register(r'repair-services', RepairServiceViewSet, basename='repairservice')
router.register(r'repair-checklists', RepairChecklistViewSet, basename='repairchecklist')
router.register(r'repair-attachments', RepairAttachmentViewSet, basename='repairattachment')
router.register(r'repair-templates', RepairTemplateViewSet, basename='repairtemplate')

urlpatterns = [
    path('', include(router.urls)),
]
