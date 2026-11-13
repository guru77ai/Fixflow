"""
Views for Suppliers module
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction
from .models import (
    SupplierCategory, Supplier, SupplierContact, SupplierDocument
)
from .forms import (
    SupplierCategoryForm, SupplierForm, SupplierContactForm, SupplierDocumentForm
)
from apps.core.mixins import OrganizationContextMixin, BranchContextMixin


# Supplier Category Views
class SupplierCategoryListView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, ListView):
    """List all supplier categories."""
    model = SupplierCategory
    template_name = 'suppliers/suppliercategory_list.html'
    context_object_name = 'categories'
    paginate_by = 20
    
    def get_queryset(self):
        return SupplierCategory.objects.filter(
            organization=self.request.organization
        ).order_by('code')


class SupplierCategoryCreateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, CreateView):
    """Create a new supplier category."""
    model = SupplierCategory
    form_class = SupplierCategoryForm
    template_name = 'suppliers/suppliercategory_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organization'] = self.request.organization
        return kwargs
    
    def form_valid(self, form):
        form.instance.organization = self.request.organization
        return super().form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Supplier category created successfully!')
        return reverse_lazy('suppliers:suppliercategory_list')


class SupplierCategoryUpdateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, UpdateView):
    """Update a supplier category."""
    model = SupplierCategory
    form_class = SupplierCategoryForm
    template_name = 'suppliers/suppliercategory_form.html'
    
    def get_queryset(self):
        return SupplierCategory.objects.filter(
            organization=self.request.organization
        )
    
    def get_success_url(self):
        messages.success(self.request, 'Supplier category updated successfully!')
        return reverse_lazy('suppliers:suppliercategory_list')


class SupplierCategoryDeleteView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, DeleteView):
    """Delete a supplier category."""
    model = SupplierCategory
    template_name = 'suppliers/suppliercategory_confirm_delete.html'
    context_object_name = 'category'
    
    def get_queryset(self):
        return SupplierCategory.objects.filter(
            organization=self.request.organization
        )
    
    def get_success_url(self):
        messages.success(self.request, 'Supplier category deleted successfully!')
        return reverse_lazy('suppliers:suppliercategory_list')


# Supplier Views
class SupplierListView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, ListView):
    """List all suppliers."""
    model = Supplier
    template_name = 'suppliers/supplier_list.html'
    context_object_name = 'suppliers'
    paginate_by = 20
    
    def get_queryset(self):
        return Supplier.objects.filter(
            organization=self.request.organization
        ).order_by('code')


class SupplierDetailView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, DetailView):
    """Supplier detail view."""
    model = Supplier
    template_name = 'suppliers/supplier_detail.html'
    context_object_name = 'supplier'
    
    def get_queryset(self):
        return Supplier.objects.filter(
            organization=self.request.organization
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = SupplierContact.objects.filter(
            supplier=self.object
        )
        context['documents'] = SupplierDocument.objects.filter(
            supplier=self.object
        )
        context['purchases'] = []  # Will be populated with purchase orders when available
        return context


class SupplierCreateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, CreateView):
    """Create a new supplier."""
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/supplier_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organization'] = self.request.organization
        return kwargs
    
    def form_valid(self, form):
        form.instance.organization = self.request.organization
        return super().form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Supplier created successfully!')
        return reverse_lazy('suppliers:supplier_detail', kwargs={'pk': self.object.pk})


class SupplierUpdateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, UpdateView):
    """Update a supplier."""
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/supplier_form.html'
    
    def get_queryset(self):
        return Supplier.objects.filter(
            organization=self.request.organization
        )
    
    def get_success_url(self):
        messages.success(self.request, 'Supplier updated successfully!')
        return reverse_lazy('suppliers:supplier_detail', kwargs={'pk': self.object.pk})


class SupplierDeleteView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, DeleteView):
    """Delete a supplier."""
    model = Supplier
    template_name = 'suppliers/supplier_confirm_delete.html'
    context_object_name = 'supplier'
    
    def get_queryset(self):
        return Supplier.objects.filter(
            organization=self.request.organization
        )
    
    def get_success_url(self):
        messages.success(self.request, 'Supplier deleted successfully!')
        return reverse_lazy('suppliers:supplier_list')


# Supplier Contact Views
class SupplierContactListView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, ListView):
    """List all contacts for a supplier."""
    model = SupplierContact
    template_name = 'suppliers/suppliercontact_list.html'
    context_object_name = 'contacts'
    
    def get_queryset(self):
        supplier_pk = self.kwargs.get('supplier_pk')
        return SupplierContact.objects.filter(
            supplier__organization=self.request.organization,
            supplier_id=supplier_pk
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        supplier_pk = self.kwargs.get('supplier_pk')
        context['supplier'] = get_object_or_404(
            Supplier.objects.filter(organization=self.request.organization),
            pk=supplier_pk
        )
        return context


class SupplierContactCreateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, CreateView):
    """Create a new supplier contact."""
    model = SupplierContact
    form_class = SupplierContactForm
    template_name = 'suppliers/suppliercontact_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        supplier_pk = self.kwargs.get('supplier_pk')
        supplier = get_object_or_404(
            Supplier.objects.filter(organization=self.request.organization),
            pk=supplier_pk
        )
        kwargs['supplier'] = supplier
        return kwargs
    
    def form_valid(self, form):
        supplier_pk = self.kwargs.get('supplier_pk')
        supplier = get_object_or_404(
            Supplier.objects.filter(organization=self.request.organization),
            pk=supplier_pk
        )
        form.instance.supplier = supplier
        return super().form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Supplier contact created successfully!')
        return reverse_lazy('suppliers:suppliercontact_list', kwargs={'supplier_pk': self.object.supplier.pk})


class SupplierContactUpdateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, UpdateView):
    """Update a supplier contact."""
    model = SupplierContact
    form_class = SupplierContactForm
    template_name = 'suppliers/suppliercontact_form.html'
    
    def get_queryset(self):
        supplier_pk = self.kwargs.get('supplier_pk')
        return SupplierContact.objects.filter(
            supplier__organization=self.request.organization,
            supplier_id=supplier_pk
        )
    
    def get_success_url(self):
        messages.success(self.request, 'Supplier contact updated successfully!')
        return reverse_lazy('suppliers:suppliercontact_list', kwargs={'supplier_pk': self.object.supplier.pk})


class SupplierContactDeleteView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, DeleteView):
    """Delete a supplier contact."""
    model = SupplierContact
    template_name = 'suppliers/suppliercontact_confirm_delete.html'
    context_object_name = 'contact'
    
    def get_queryset(self):
        supplier_pk = self.kwargs.get('supplier_pk')
        return SupplierContact.objects.filter(
            supplier__organization=self.request.organization,
            supplier_id=supplier_pk
        )
    
    def get_success_url(self):
        messages.success(self.request, 'Supplier contact deleted successfully!')
        return reverse_lazy('suppliers:suppliercontact_list', kwargs={'supplier_pk': self.object.supplier.pk})


# Supplier Document Views
class SupplierDocumentListView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, ListView):
    """List all documents for a supplier."""
    model = SupplierDocument
    template_name = 'suppliers/supplierdocument_list.html'
    context_object_name = 'documents'
    
    def get_queryset(self):
        supplier_pk = self.kwargs.get('supplier_pk')
        return SupplierDocument.objects.filter(
            supplier__organization=self.request.organization,
            supplier_id=supplier_pk
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        supplier_pk = self.kwargs.get('supplier_pk')
        context['supplier'] = get_object_or_404(
            Supplier.objects.filter(organization=self.request.organization),
            pk=supplier_pk
        )
        return context


class SupplierDocumentCreateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, CreateView):
    """Create a new supplier document."""
    model = SupplierDocument
    form_class = SupplierDocumentForm
    template_name = 'suppliers/supplierdocument_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        supplier_pk = self.kwargs.get('supplier_pk')
        supplier = get_object_or_404(
            Supplier.objects.filter(organization=self.request.organization),
            pk=supplier_pk
        )
        kwargs['supplier'] = supplier
        return kwargs
    
    def form_valid(self, form):
        supplier_pk = self.kwargs.get('supplier_pk')
        supplier = get_object_or_404(
            Supplier.objects.filter(organization=self.request.organization),
            pk=supplier_pk
        )
        form.instance.supplier = supplier
        form.instance.organization = self.request.organization
        return super().form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Supplier document created successfully!')
        return reverse_lazy('suppliers:supplierdocument_list', kwargs={'supplier_pk': self.object.supplier.pk})


class SupplierDocumentDeleteView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, DeleteView):
    """Delete a supplier document."""
    model = SupplierDocument
    template_name = 'suppliers/supplierdocument_confirm_delete.html'
    context_object_name = 'document'
    
    def get_queryset(self):
        supplier_pk = self.kwargs.get('supplier_pk')
        return SupplierDocument.objects.filter(
            supplier__organization=self.request.organization,
            supplier_id=supplier_pk
        )
    
    def get_success_url(self):
        messages.success(self.request, 'Supplier document deleted successfully!')
        return reverse_lazy('suppliers:supplierdocument_list', kwargs={'supplier_pk': self.object.supplier.pk})
