"""
Views for CRM module
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
    Customer, Device, CustomerType, CustomerSource,
    CustomerGroup, DeviceBrand, DeviceModel, DeviceCategory,
    CustomerCommunication, CustomerDocument
)
from .forms import (
    CustomerForm, DeviceForm, CustomerTypeForm, CustomerSourceForm,
    CustomerGroupForm, DeviceBrandForm, DeviceModelForm, DeviceCategoryForm,
    CustomerCommunicationForm, CustomerDocumentForm
)
from .selectors import (
    CustomerSelector, DeviceSelector, CustomerTypeSelector,
    CustomerSourceSelector, CustomerGroupSelector, DeviceBrandSelector,
    DeviceModelSelector, DeviceCategorySelector, CommunicationSelector,
    DocumentSelector
)
from .services import (
    CustomerService, DeviceService, CommunicationService, DocumentService
)
from apps.core.mixins import OrganizationContextMixin, BranchContextMixin
import json


# Customer Views
class CustomerListView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, ListView):
    """List all customers."""
    model = Customer
    template_name = 'crm/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = CustomerSelector.get_all_customers(
            organization=self.request.organization,
            branch=self.request.branch,
            status=self.request.GET.get('status'),
            search=self.request.GET.get('search')
        )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = CustomerSelector.get_customer_statistics(self.request.organization)
        context['status_choices'] = Customer.CUSTOMER_STATUS_CHOICES
        return context


class CustomerDetailView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, DetailView):
    """Customer detail view."""
    model = Customer
    template_name = 'crm/customer_detail.html'
    context_object_name = 'customer'
    
    def get_queryset(self):
        return Customer.objects.filter(organization=self.request.organization)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.object
        context['devices'] = DeviceSelector.get_devices_by_customer(customer)
        context['communications'] = CommunicationSelector.get_communications_by_customer(customer)
        context['documents'] = DocumentSelector.get_documents_by_customer(customer)
        context['stats'] = CustomerService.get_customer_statistics(customer)
        return context


class CustomerCreateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, CreateView):
    """Create a new customer."""
    model = Customer
    form_class = CustomerForm
    template_name = 'crm/customer_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organization'] = self.request.organization
        kwargs['branch'] = self.request.branch
        return kwargs
    
    def form_valid(self, form):
        form.instance.organization = self.request.organization
        form.instance.branch = self.request.branch
        return super().form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Customer created successfully!')
        return reverse_lazy('crm:customer_detail', kwargs={'pk': self.object.pk})


class CustomerUpdateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, UpdateView):
    """Update a customer."""
    model = Customer
    form_class = CustomerForm
    template_name = 'crm/customer_form.html'
    
    def get_queryset(self):
        return Customer.objects.filter(organization=self.request.organization)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organization'] = self.request.organization
        kwargs['branch'] = self.request.branch
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, 'Customer updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('crm:customer_detail', kwargs={'pk': self.object.pk})


class CustomerDeleteView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, DeleteView):
    """Delete a customer."""
    model = Customer
    template_name = 'crm/customer_confirm_delete.html'
    
    def get_queryset(self):
        return Customer.objects.filter(organization=self.request.organization)
    
    def get_success_url(self):
        messages.success(self.request, 'Customer deleted successfully!')
        return reverse_lazy('crm:customer_list')


# Device Views
class DeviceListView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, ListView):
    """List all devices."""
    model = Device
    template_name = 'crm/device_list.html'
    context_object_name = 'devices'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = DeviceSelector.get_all_devices(
            organization=self.request.organization,
            branch=self.request.branch,
            customer=self.request.GET.get('customer'),
            status=self.request.GET.get('status'),
            search=self.request.GET.get('search')
        )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = DeviceSelector.get_device_statistics(self.request.organization)
        context['status_choices'] = Device.DEVICE_STATUS_CHOICES
        return context


class DeviceDetailView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, DetailView):
    """Device detail view."""
    model = Device
    template_name = 'crm/device_detail.html'
    context_object_name = 'device'
    
    def get_queryset(self):
        return Device.objects.filter(organization=self.request.organization)


class DeviceCreateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, CreateView):
    """Create a new device."""
    model = Device
    form_class = DeviceForm
    template_name = 'crm/device_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organization'] = self.request.organization
        kwargs['branch'] = self.request.branch
        return kwargs
    
    def form_valid(self, form):
        form.instance.organization = self.request.organization
        form.instance.branch = self.request.branch
        return super().form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Device created successfully!')
        return reverse_lazy('crm:device_detail', kwargs={'pk': self.object.pk})


class DeviceUpdateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, UpdateView):
    """Update a device."""
    model = Device
    form_class = DeviceForm
    template_name = 'crm/device_form.html'
    
    def get_queryset(self):
        return Device.objects.filter(organization=self.request.organization)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organization'] = self.request.organization
        kwargs['branch'] = self.request.branch
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, 'Device updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('crm:device_detail', kwargs={'pk': self.object.pk})


# Customer Type Views
class CustomerTypeListView(LoginRequiredMixin, ListView):
    """List all customer types."""
    model = CustomerType
    template_name = 'crm/customertype_list.html'
    context_object_name = 'types'
    paginate_by = 20


class CustomerTypeCreateView(LoginRequiredMixin, CreateView):
    """Create a new customer type."""
    model = CustomerType
    form_class = CustomerTypeForm
    template_name = 'crm/customertype_form.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Customer type created successfully!')
        return reverse_lazy('crm:customertype_list')


class CustomerTypeUpdateView(LoginRequiredMixin, UpdateView):
    """Update a customer type."""
    model = CustomerType
    form_class = CustomerTypeForm
    template_name = 'crm/customertype_form.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Customer type updated successfully!')
        return reverse_lazy('crm:customertype_list')


# Device Brand Views
class DeviceBrandListView(LoginRequiredMixin, ListView):
    """List all device brands."""
    model = DeviceBrand
    template_name = 'crm/devicebrand_list.html'
    context_object_name = 'brands'
    paginate_by = 20


class DeviceBrandCreateView(LoginRequiredMixin, CreateView):
    """Create a new device brand."""
    model = DeviceBrand
    form_class = DeviceBrandForm
    template_name = 'crm/devicebrand_form.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Device brand created successfully!')
        return reverse_lazy('crm:devicebrand_list')


# API Views
class CustomerAPIView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin):
    """API endpoints for customers."""
    
    def get(self, request, pk=None):
        """Get customer(s)."""
        if pk:
            customer = get_object_or_404(Customer, pk=pk, organization=request.organization)
            data = {
                'id': str(customer.id),
                'code': customer.code,
                'full_name': customer.full_name,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'company_name': customer.company_name,
                'phone': customer.phone,
                'mobile': customer.mobile,
                'email': customer.email,
                'credit_balance': str(customer.credit_balance),
                'status': customer.status,
                'created_at': customer.created_at.isoformat() if customer.created_at else None,
            }
            return JsonResponse(data)
        else:
            customers = CustomerSelector.get_all_customers(
                organization=request.organization,
                branch=request.branch,
                search=request.GET.get('search'),
                limit=20
            )
            data = [{
                'id': str(c.id),
                'code': c.code,
                'full_name': c.full_name,
                'phone': c.phone,
                'email': c.email,
                'status': c.status,
            } for c in customers]
            return JsonResponse({'results': data})
    
    def post(self, request):
        """Create a customer."""
        try:
            data = json.loads(request.body)
            customer = CustomerService.create_customer(
                data=data,
                organization=request.organization,
                branch=request.branch,
                created_by=request.user
            )
            return JsonResponse({
                'success': True,
                'id': str(customer.id),
                'code': customer.code
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)


class DeviceAPIView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin):
    """API endpoints for devices."""
    
    def get(self, request, pk=None):
        """Get device(s)."""
        if pk:
            device = get_object_or_404(Device, pk=pk, organization=request.organization)
            data = {
                'id': str(device.id),
                'name': device.name,
                'customer': {
                    'id': str(device.customer.id),
                    'code': device.customer.code,
                    'full_name': device.customer.full_name
                },
                'imei_1': device.imei_1,
                'imei_2': device.imei_2,
                'serial_number': device.serial_number,
                'model': device.model.name if device.model else None,
                'brand': device.brand.name if device.brand else None,
                'status': device.status,
                'tag': device.tag,
            }
            return JsonResponse(data)
        else:
            devices = DeviceSelector.get_all_devices(
                organization=request.organization,
                branch=request.branch,
                search=request.GET.get('search'),
                limit=20
            )
            data = [{
                'id': str(d.id),
                'name': d.name,
                'customer': d.customer.full_name,
                'imei': d.imei_1 or d.imei_2,
                'serial': d.serial_number,
                'status': d.status,
            } for d in devices]
            return JsonResponse({'results': data})
    
    def post(self, request):
        """Create a device."""
        try:
            data = json.loads(request.body)
            customer = get_object_or_404(Customer, pk=data.get('customer_id'), organization=request.organization)
            device = DeviceService.create_device(
                data=data,
                customer=customer,
                organization=request.organization,
                branch=request.branch
            )
            return JsonResponse({
                'success': True,
                'id': str(device.id)
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)


# Quick Customer Creation (for POS and Repair)
@csrf_exempt
@transaction.atomic
def quick_create_customer(request):
    """Quick customer creation endpoint for POS and Repair modules."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Check if customer already exists
            phone = data.get('phone')
            if phone:
                existing = CustomerService.get_customer_by_phone(
                    phone,
                    request.organization
                )
                if existing:
                    return JsonResponse({
                        'success': True,
                        'customer_id': str(existing.id),
                        'code': existing.code,
                        'name': existing.full_name
                    })
            
            # Create new customer
            customer_data = {
                'code': data.get('code'),
                'first_name': data.get('first_name', 'Unknown'),
                'last_name': data.get('last_name', ''),
                'phone': phone,
                'mobile': data.get('mobile'),
                'email': data.get('email'),
                'address_line_1': data.get('address'),
            }
            
            customer = CustomerService.create_customer(
                data=customer_data,
                organization=request.organization,
                branch=request.branch,
                created_by=request.user
            )
            
            return JsonResponse({
                'success': True,
                'customer_id': str(customer.id),
                'code': customer.code,
                'name': customer.full_name
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


# Search endpoints
class CustomerSearchView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin):
    """Customer search endpoint."""
    
    def get(self, request):
        query = request.GET.get('q', '')
        limit = int(request.GET.get('limit', 10))
        
        customers = CustomerService.search_customers(
            query=query,
            organization=request.organization,
            branch=request.branch,
            limit=limit
        )
        
        results = [{
            'id': str(c.id),
            'code': c.code,
            'name': c.full_name,
            'phone': c.phone,
            'email': c.email,
            'address': c.address_line_1,
            'balance': str(c.credit_balance),
        } for c in customers]
        
        return JsonResponse({'results': results})


class DeviceSearchView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin):
    """Device search endpoint."""
    
    def get(self, request):
        query = request.GET.get('q', '')
        customer_id = request.GET.get('customer_id')
        limit = int(request.GET.get('limit', 10))
        
        customer = None
        if customer_id:
            customer = get_object_or_404(Customer, pk=customer_id, organization=request.organization)
        
        devices = DeviceService.search_devices(
            query=query,
            organization=request.organization,
            customer=customer,
            limit=limit
        )
        
        results = [{
            'id': str(d.id),
            'name': d.name,
            'imei': d.imei_1 or d.imei_2,
            'serial': d.serial_number,
            'model': d.model.name if d.model else d.name,
            'customer': d.customer.full_name,
        } for d in devices]
        
        return JsonResponse({'results': results})
