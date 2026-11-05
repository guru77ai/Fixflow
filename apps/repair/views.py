"""
Views for Repair module
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import (
    RepairOrder, RepairPart, RepairService, RepairChecklist,
    RepairAttachment, RepairOrderHistory, RepairTemplate,
    RepairStatus, RepairPriority, RepairCategory, RepairType
)
from .forms import (
    RepairOrderForm, RepairPartForm, RepairServiceForm, RepairChecklistForm,
    RepairAttachmentForm, RepairTemplateForm, RepairStatusForm, RepairPriorityForm,
    RepairCategoryForm, RepairTypeForm
)
from .selectors import (
    RepairOrderSelector, RepairPartSelector, RepairServiceSelector,
    RepairChecklistSelector, RepairAttachmentSelector, RepairHistorySelector,
    RepairTemplateSelector, RepairStatusSelector, RepairPrioritySelector,
    RepairCategorySelector, RepairTypeSelector
)
from .services import (
    RepairOrderService, RepairPartService, RepairServiceService,
    RepairChecklistService, RepairAttachmentService, RepairTemplateService,
    RepairStatisticsService
)
from apps.core.mixins import OrganizationContextMixin, BranchContextMixin
import json


# Repair Order Views
class RepairOrderListView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, ListView):
    """List all repair orders."""
    model = RepairOrder
    template_name = 'repair/repairorder_list.html'
    context_object_name = 'repair_orders'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = RepairOrderSelector.get_all_orders(
            organization=self.request.organization,
            branch=self.request.branch,
            status=self.request.GET.get('status'),
            priority=self.request.GET.get('priority'),
            technician=self.request.GET.get('technician'),
            search=self.request.GET.get('search'),
            start_date=self.request.GET.get('start_date'),
            end_date=self.request.GET.get('end_date')
        )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = RepairOrderSelector.get_statistics(
            self.request.organization,
            self.request.branch
        )
        context['statuses'] = RepairStatus.objects.all()
        context['priorities'] = RepairPriority.objects.all()
        return context


class RepairOrderDetailView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, DetailView):
    """Repair order detail view."""
    model = RepairOrder
    template_name = 'repair/repairorder_detail.html'
    context_object_name = 'repair_order'
    
    def get_queryset(self):
        return RepairOrder.objects.filter(organization=self.request.organization)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        repair_order = self.object
        context['parts'] = RepairPartSelector.get_parts_by_repair_order(repair_order)
        context['services'] = RepairServiceSelector.get_services_by_repair_order(repair_order)
        context['checklists'] = RepairChecklistSelector.get_checklists_by_repair_order(repair_order)
        context['attachments'] = RepairAttachmentSelector.get_attachments_by_repair_order(repair_order)
        context['history'] = RepairHistorySelector.get_history_by_repair_order(repair_order)
        context['checklist_progress'] = RepairChecklistService.get_checklist_progress(repair_order)
        return context


class RepairOrderCreateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, CreateView):
    """Create a new repair order."""
    model = RepairOrder
    form_class = RepairOrderForm
    template_name = 'repair/repairorder_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organization'] = self.request.organization
        kwargs['branch'] = self.request.branch
        return kwargs
    
    def form_valid(self, form):
        form.instance.organization = self.request.organization
        form.instance.branch = self.request.branch
        form.instance.status_changed_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Repair order created successfully!')
        return reverse_lazy('repair:repairorder_detail', kwargs={'pk': self.object.pk})


class RepairOrderUpdateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, UpdateView):
    """Update a repair order."""
    model = RepairOrder
    form_class = RepairOrderForm
    template_name = 'repair/repairorder_form.html'
    
    def get_queryset(self):
        return RepairOrder.objects.filter(organization=self.request.organization)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organization'] = self.request.organization
        kwargs['branch'] = self.request.branch
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, 'Repair order updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('repair:repairorder_detail', kwargs={'pk': self.object.pk})


class RepairOrderDeleteView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, DeleteView):
    """Delete a repair order."""
    model = RepairOrder
    template_name = 'repair/repairorder_confirm_delete.html'
    
    def get_queryset(self):
        return RepairOrder.objects.filter(organization=self.request.organization)
    
    def get_success_url(self):
        messages.success(self.request, 'Repair order deleted successfully!')
        return reverse_lazy('repair:repairorder_list')


# Status change view
class RepairOrderStatusChangeView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, UpdateView):
    """Change repair order status."""
    model = RepairOrder
    fields = ['status', 'status_changed_by']
    template_name = 'repair/repairorder_status_change.html'
    
    def get_queryset(self):
        return RepairOrder.objects.filter(organization=self.request.organization)
    
    def form_valid(self, form):
        repair_order = self.object
        new_status = form.cleaned_data['status']
        
        # Update status through service to track history
        RepairOrderService.update_status(
            repair_order,
            new_status,
            changed_by=self.request.user,
            comments=form.cleaned_data.get('comments', '')
        )
        
        messages.success(self.request, f'Status changed to {new_status.name}')
        return redirect('repair:repairorder_detail', pk=repair_order.pk)
    
    def get_success_url(self):
        return reverse_lazy('repair:repairorder_detail', kwargs={'pk': self.object.pk})


# Dashboard view
class RepairDashboardView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, ListView):
    """Repair dashboard showing overview and statistics."""
    model = RepairOrder
    template_name = 'repair/dashboard.html'
    context_object_name = 'recent_orders'
    
    def get_queryset(self):
        return RepairOrderSelector.get_recent_orders(
            self.request.organization,
            self.request.branch,
            limit=10
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = RepairOrderSelector.get_statistics(
            self.request.organization,
            self.request.branch
        )
        context['overdue_orders'] = RepairOrderSelector.get_overdue_orders(
            self.request.organization,
            self.request.branch
        )[:5]
        context['unassigned_orders'] = RepairOrderSelector.get_unassigned_orders(
            self.request.organization,
            self.request.branch
        )[:5]
        context['urgent_orders'] = RepairOrderSelector.get_urgent_orders(
            self.request.organization,
            self.request.branch
        )[:5]
        return context


# Quick repair creation
@csrf_exempt
@transaction.atomic
def quick_create_repair_order(request):
    """Quick repair order creation endpoint."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Create repair order
            repair_order = RepairOrderService.create_repair_order(
                data=data,
                organization=request.organization,
                branch=request.branch,
                created_by=request.user
            )
            
            return JsonResponse({
                'success': True,
                'repair_order_id': str(repair_order.id),
                'order_number': repair_order.order_number
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


# API Views
class RepairOrderAPIView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin):
    """API endpoints for repair orders."""
    
    def get(self, request, pk=None):
        """Get repair order(s)."""
        if pk:
            repair_order = get_object_or_404(
                RepairOrder,
                pk=pk,
                organization=request.organization
            )
            data = {
                'id': str(repair_order.id),
                'order_number': repair_order.order_number,
                'customer': {
                    'id': str(repair_order.customer.id),
                    'code': repair_order.customer.code,
                    'name': repair_order.customer.full_name,
                    'phone': repair_order.customer.phone
                },
                'device': repair_order.device_display,
                'status': repair_order.status.name,
                'priority': repair_order.priority.name,
                'issue_description': repair_order.issue_description,
                'quotation_amount': str(repair_order.quotation_amount),
                'final_amount': str(repair_order.final_amount),
                'balance': str(repair_order.balance),
                'received_date': repair_order.received_date.isoformat() if repair_order.received_date else None,
                'promised_date': repair_order.promised_date.isoformat() if repair_order.promised_date else None,
                'completed_date': repair_order.completed_date.isoformat() if repair_order.completed_date else None,
                'is_overdue': repair_order.is_overdue,
                'assigned_to': str(repair_order.assigned_to) if repair_order.assigned_to else None,
            }
            return JsonResponse(data)
        else:
            repair_orders = RepairOrderSelector.get_all_orders(
                organization=request.organization,
                branch=request.branch,
                status=request.GET.get('status'),
                search=request.GET.get('search'),
                limit=20
            )
            data = [{
                'id': str(ro.id),
                'order_number': ro.order_number,
                'customer': ro.customer.full_name,
                'device': ro.device_display,
                'status': ro.status.name,
                'priority': ro.priority.name,
                'received_date': ro.received_date.isoformat() if ro.received_date else None,
                'promised_date': ro.promised_date.isoformat() if ro.promised_date else None,
                'final_amount': str(ro.final_amount),
                'is_overdue': ro.is_overdue,
            } for ro in repair_orders]
            return JsonResponse({'results': data})
    
    def post(self, request):
        """Create a repair order."""
        try:
            data = json.loads(request.body)
            repair_order = RepairOrderService.create_repair_order(
                data=data,
                organization=request.organization,
                branch=request.branch,
                created_by=request.user
            )
            return JsonResponse({
                'success': True,
                'id': str(repair_order.id),
                'order_number': repair_order.order_number
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)


class RepairStatisticsAPIView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin):
    """API endpoint for repair statistics."""
    
    def get(self, request):
        stats = RepairStatisticsService.get_statistics(
            organization=request.organization,
            branch=request.branch,
            start_date=request.GET.get('start_date'),
            end_date=request.GET.get('end_date')
        )
        
        # Convert datetime objects to strings
        data = {}
        for key, value in stats.items():
            if isinstance(value, list):
                data[key] = [
                    {
                        k: v.isoformat() if hasattr(v, 'isoformat') else v
                        for k, v in item.items()
                    }
                    for item in value
                ]
            elif hasattr(value, 'isoformat'):
                data[key] = value.isoformat()
            else:
                data[key] = value
        
        return JsonResponse(data)


# Search endpoints
class RepairOrderSearchView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin):
    """Repair order search endpoint."""
    
    def get(self, request):
        query = request.GET.get('q', '')
        limit = int(request.GET.get('limit', 10))
        
        repair_orders = RepairOrderSelector.get_all_orders(
            organization=request.organization,
            branch=request.branch,
            search=query,
            limit=limit
        )
        
        results = [{
            'id': str(ro.id),
            'order_number': ro.order_number,
            'customer': ro.customer.full_name,
            'device': ro.device_display,
            'status': ro.status.name,
            'priority': ro.priority.name,
            'received_date': ro.received_date.isoformat() if ro.received_date else None,
        } for ro in repair_orders]
        
        return JsonResponse({'results': results})


class DeviceSearchForRepairView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin):
    """Device search for repair endpoint."""
    
    def get(self, request):
        from apps.crm.models import Device
        from apps.crm.selectors import DeviceSelector
        
        query = request.GET.get('q', '')
        limit = int(request.GET.get('limit', 10))
        
        devices = DeviceSelector.search_devices(
            query=query,
            organization=request.organization,
            limit=limit
        )
        
        results = [{
            'id': str(d.id),
            'name': d.name,
            'imei': d.imei_1 or d.imei_2,
            'serial': d.serial_number,
            'customer': d.customer.full_name,
            'customer_id': str(d.customer.id),
        } for d in devices]
        
        return JsonResponse({'results': results})
