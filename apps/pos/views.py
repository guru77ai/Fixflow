"""
Views for POS module
"""
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from .models import Sale, CashRegister, POSSession, PaymentMethod
from .forms import SaleForm, CashRegisterForm
from .selectors import SaleSelector, CashRegisterSelector
from .services import SaleService, CashRegisterService
from apps.core.mixins import OrganizationContextMixin, BranchContextMixin
import json


class SaleListView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, ListView):
    model = Sale
    template_name = 'pos/sale_list.html'
    context_object_name = 'sales'
    paginate_by = 20
    
    def get_queryset(self):
        return SaleSelector.get_all_sales(
            organization=self.request.organization,
            branch=self.request.branch,
            status=self.request.GET.get('status'),
            search=self.request.GET.get('search'),
            start_date=self.request.GET.get('start_date'),
            end_date=self.request.GET.get('end_date')
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = SaleSelector.get_statistics(self.request.organization, self.request.branch)
        return context


class SaleDetailView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, DetailView):
    model = Sale
    template_name = 'pos/sale_detail.html'
    context_object_name = 'sale'
    
    def get_queryset(self):
        return Sale.objects.filter(organization=self.request.organization)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sale = self.object
        context['items'] = sale.items.all()
        context['payments'] = sale.payments.all()
        context['receipt'] = sale.receipt
        return context


class SaleCreateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'pos/sale_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organization'] = self.request.organization
        kwargs['branch'] = self.request.branch
        return kwargs
    
    def form_valid(self, form):
        form.instance.organization = self.request.organization
        form.instance.branch = self.request.branch
        form.instance.sold_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Sale created successfully!')
        return reverse_lazy('pos:sale_detail', kwargs={'pk': self.object.pk})


class SaleAPIView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin):
    def get(self, request, pk=None):
        if pk:
            sale = get_object_or_404(Sale, pk=pk, organization=request.organization)
            data = {
                'id': str(sale.id),
                'sale_number': sale.sale_number,
                'customer': str(sale.customer) if sale.customer else None,
                'total_amount': str(sale.total_amount),
                'status': sale.status,
                'created_at': sale.created_at.isoformat() if sale.created_at else None,
            }
            return JsonResponse(data)
        else:
            sales = SaleSelector.get_all_sales(
                organization=request.organization,
                branch=request.branch,
                limit=20
            )
            data = [{
                'id': str(s.id),
                'sale_number': s.sale_number,
                'customer': str(s.customer) if s.customer else 'Walk-in',
                'total_amount': str(s.total_amount),
                'status': s.status,
                'created_at': s.created_at.isoformat() if s.created_at else None,
            } for s in sales]
            return JsonResponse({'results': data})
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            sale = SaleService.create_sale(
                data=data,
                organization=request.organization,
                branch=request.branch,
                created_by=request.user
            )
            return JsonResponse({
                'success': True,
                'sale_id': str(sale.id),
                'sale_number': sale.sale_number
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)


class POSDashboardView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, ListView):
    model = Sale
    template_name = 'pos/dashboard.html'
    context_object_name = 'recent_sales'
    
    def get_queryset(self):
        return SaleSelector.get_all_sales(
            organization=self.request.organization,
            branch=self.request.branch
        )[:10]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = SaleSelector.get_statistics(self.request.organization, self.request.branch)
        context['open_registers'] = CashRegisterSelector.get_open_registers(self.request.organization, self.request.branch)
        return context
