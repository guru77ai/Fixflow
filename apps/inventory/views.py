"""
Views for Inventory module
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction
from .models import (
    Warehouse, ProductCategory, ProductBrand, UnitOfMeasure,
    Product, ProductSerialNumber, StockMovement, StockTransfer,
    StockTransferItem, StockAdjustment, StockAdjustmentItem,
    Service, ServiceCategory
)
from .forms import (
    WarehouseForm, ProductCategoryForm, ProductBrandForm, UnitOfMeasureForm,
    ProductForm, ServiceForm, ServiceCategoryForm
)
from apps.core.mixins import OrganizationContextMixin, BranchContextMixin


# Warehouse Views
class WarehouseListView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, ListView):
    """List all warehouses."""
    model = Warehouse
    template_name = 'inventory/warehouse_list.html'
    context_object_name = 'warehouses'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Warehouse.objects.filter(
            organization=self.request.organization,
            branch=self.request.branch
        ).order_by('code')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = {
            'total': self.get_queryset().count(),
            'active': self.get_queryset().filter(is_active=True).count(),
        }
        return context


class WarehouseDetailView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, DetailView):
    """Warehouse detail view."""
    model = Warehouse
    template_name = 'inventory/warehouse_detail.html'
    context_object_name = 'warehouse'
    
    def get_queryset(self):
        return Warehouse.objects.filter(
            organization=self.request.organization,
            branch=self.request.branch
        )


class WarehouseCreateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, CreateView):
    """Create a new warehouse."""
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'inventory/warehouse_form.html'
    
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
        messages.success(self.request, 'Warehouse created successfully!')
        return reverse_lazy('inventory:warehouse_detail', kwargs={'pk': self.object.pk})


class WarehouseUpdateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, UpdateView):
    """Update a warehouse."""
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'inventory/warehouse_form.html'
    
    def get_queryset(self):
        return Warehouse.objects.filter(
            organization=self.request.organization,
            branch=self.request.branch
        )
    
    def get_success_url(self):
        messages.success(self.request, 'Warehouse updated successfully!')
        return reverse_lazy('inventory:warehouse_detail', kwargs={'pk': self.object.pk})


class WarehouseDeleteView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, DeleteView):
    """Delete a warehouse."""
    model = Warehouse
    template_name = 'inventory/warehouse_confirm_delete.html'
    context_object_name = 'warehouse'
    
    def get_queryset(self):
        return Warehouse.objects.filter(
            organization=self.request.organization,
            branch=self.request.branch
        )
    
    def get_success_url(self):
        messages.success(self.request, 'Warehouse deleted successfully!')
        return reverse_lazy('inventory:warehouse_list')


# Product Category Views
class ProductCategoryListView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, ListView):
    """List all product categories."""
    model = ProductCategory
    template_name = 'inventory/productcategory_list.html'
    context_object_name = 'categories'
    paginate_by = 20
    
    def get_queryset(self):
        return ProductCategory.objects.filter(
            organization=self.request.organization,
            branch=self.request.branch
        ).order_by('code')


class ProductCategoryCreateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, CreateView):
    """Create a new product category."""
    model = ProductCategory
    form_class = ProductCategoryForm
    template_name = 'inventory/productcategory_form.html'
    
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
        messages.success(self.request, 'Product category created successfully!')
        return reverse_lazy('inventory:productcategory_list')


class ProductCategoryUpdateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, UpdateView):
    """Update a product category."""
    model = ProductCategory
    form_class = ProductCategoryForm
    template_name = 'inventory/productcategory_form.html'
    
    def get_queryset(self):
        return ProductCategory.objects.filter(
            organization=self.request.organization,
            branch=self.request.branch
        )
    
    def get_success_url(self):
        messages.success(self.request, 'Product category updated successfully!')
        return reverse_lazy('inventory:productcategory_list')


class ProductCategoryDeleteView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, DeleteView):
    """Delete a product category."""
    model = ProductCategory
    template_name = 'inventory/productcategory_confirm_delete.html'
    context_object_name = 'category'
    
    def get_queryset(self):
        return ProductCategory.objects.filter(
            organization=self.request.organization,
            branch=self.request.branch
        )
    
    def get_success_url(self):
        messages.success(self.request, 'Product category deleted successfully!')
        return reverse_lazy('inventory:productcategory_list')


# Product Brand Views
class ProductBrandListView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, ListView):
    """List all product brands."""
    model = ProductBrand
    template_name = 'inventory/productbrand_list.html'
    context_object_name = 'brands'
    paginate_by = 20
    
    def get_queryset(self):
        return ProductBrand.objects.filter(
            organization=self.request.organization
        ).order_by('code')


class ProductBrandCreateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, CreateView):
    """Create a new product brand."""
    model = ProductBrand
    form_class = ProductBrandForm
    template_name = 'inventory/productbrand_form.html'
    
    def form_valid(self, form):
        form.instance.organization = self.request.organization
        return super().form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Product brand created successfully!')
        return reverse_lazy('inventory:productbrand_list')


class ProductBrandUpdateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, UpdateView):
    """Update a product brand."""
    model = ProductBrand
    form_class = ProductBrandForm
    template_name = 'inventory/productbrand_form.html'
    
    def get_queryset(self):
        return ProductBrand.objects.filter(
            organization=self.request.organization
        )
    
    def get_success_url(self):
        messages.success(self.request, 'Product brand updated successfully!')
        return reverse_lazy('inventory:productbrand_list')


class ProductBrandDeleteView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, DeleteView):
    """Delete a product brand."""
    model = ProductBrand
    template_name = 'inventory/productbrand_confirm_delete.html'
    context_object_name = 'brand'
    
    def get_queryset(self):
        return ProductBrand.objects.filter(
            organization=self.request.organization
        )
    
    def get_success_url(self):
        messages.success(self.request, 'Product brand deleted successfully!')
        return reverse_lazy('inventory:productbrand_list')


# Unit of Measure Views
class UnitOfMeasureListView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, ListView):
    """List all units of measure."""
    model = UnitOfMeasure
    template_name = 'inventory/unitofmeasure_list.html'
    context_object_name = 'units'
    paginate_by = 20
    
    def get_queryset(self):
        return UnitOfMeasure.objects.all().order_by('code')


class UnitOfMeasureCreateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, CreateView):
    """Create a new unit of measure."""
    model = UnitOfMeasure
    form_class = UnitOfMeasureForm
    template_name = 'inventory/unitofmeasure_form.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Unit of measure created successfully!')
        return reverse_lazy('inventory:unitofmeasure_list')


class UnitOfMeasureUpdateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, UpdateView):
    """Update a unit of measure."""
    model = UnitOfMeasure
    form_class = UnitOfMeasureForm
    template_name = 'inventory/unitofmeasure_form.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Unit of measure updated successfully!')
        return reverse_lazy('inventory:unitofmeasure_list')


class UnitOfMeasureDeleteView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, DeleteView):
    """Delete a unit of measure."""
    model = UnitOfMeasure
    template_name = 'inventory/unitofmeasure_confirm_delete.html'
    context_object_name = 'unit'
    
    def get_success_url(self):
        messages.success(self.request, 'Unit of measure deleted successfully!')
        return reverse_lazy('inventory:unitofmeasure_list')


# Product Views
class ProductListView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, ListView):
    """List all products."""
    model = Product
    template_name = 'inventory/product_list.html'
    context_object_name = 'products'
    paginate_by = 20
    
    def get_queryset(self):
        return Product.objects.filter(
            organization=self.request.organization,
            branch=self.request.branch
        ).order_by('code')


class ProductDetailView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, DetailView):
    """Product detail view."""
    model = Product
    template_name = 'inventory/product_detail.html'
    context_object_name = 'product'
    
    def get_queryset(self):
        return Product.objects.filter(
            organization=self.request.organization,
            branch=self.request.branch
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['serial_numbers'] = ProductSerialNumber.objects.filter(
            product=self.object
        )
        context['stock_movements'] = StockMovement.objects.filter(
            product=self.object
        ).order_by('-date')[:10]
        return context


class ProductCreateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, CreateView):
    """Create a new product."""
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    
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
        messages.success(self.request, 'Product created successfully!')
        return reverse_lazy('inventory:product_detail', kwargs={'pk': self.object.pk})


class ProductUpdateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, UpdateView):
    """Update a product."""
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    
    def get_queryset(self):
        return Product.objects.filter(
            organization=self.request.organization,
            branch=self.request.branch
        )
    
    def get_success_url(self):
        messages.success(self.request, 'Product updated successfully!')
        return reverse_lazy('inventory:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, DeleteView):
    """Delete a product."""
    model = Product
    template_name = 'inventory/product_confirm_delete.html'
    context_object_name = 'product'
    
    def get_queryset(self):
        return Product.objects.filter(
            organization=self.request.organization,
            branch=self.request.branch
        )
    
    def get_success_url(self):
        messages.success(self.request, 'Product deleted successfully!')
        return reverse_lazy('inventory:product_list')


# Service Category Views
class ServiceCategoryListView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, ListView):
    """List all service categories."""
    model = ServiceCategory
    template_name = 'inventory/servicecategory_list.html'
    context_object_name = 'categories'
    paginate_by = 20
    
    def get_queryset(self):
        return ServiceCategory.objects.filter(
            organization=self.request.organization,
            branch=self.request.branch
        ).order_by('code')


class ServiceCategoryCreateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, CreateView):
    """Create a new service category."""
    model = ServiceCategory
    form_class = ServiceCategoryForm
    template_name = 'inventory/servicecategory_form.html'
    
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
        messages.success(self.request, 'Service category created successfully!')
        return reverse_lazy('inventory:servicecategory_list')


class ServiceCategoryUpdateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, UpdateView):
    """Update a service category."""
    model = ServiceCategory
    form_class = ServiceCategoryForm
    template_name = 'inventory/servicecategory_form.html'
    
    def get_queryset(self):
        return ServiceCategory.objects.filter(
            organization=self.request.organization,
            branch=self.request.branch
        )
    
    def get_success_url(self):
        messages.success(self.request, 'Service category updated successfully!')
        return reverse_lazy('inventory:servicecategory_list')


class ServiceCategoryDeleteView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, DeleteView):
    """Delete a service category."""
    model = ServiceCategory
    template_name = 'inventory/servicecategory_confirm_delete.html'
    context_object_name = 'category'
    
    def get_queryset(self):
        return ServiceCategory.objects.filter(
            organization=self.request.organization,
            branch=self.request.branch
        )
    
    def get_success_url(self):
        messages.success(self.request, 'Service category deleted successfully!')
        return reverse_lazy('inventory:servicecategory_list')


# Service Views
class ServiceListView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, ListView):
    """List all services."""
    model = Service
    template_name = 'inventory/service_list.html'
    context_object_name = 'services'
    paginate_by = 20
    
    def get_queryset(self):
        return Service.objects.filter(
            organization=self.request.organization,
            branch=self.request.branch
        ).order_by('code')


class ServiceCreateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, CreateView):
    """Create a new service."""
    model = Service
    form_class = ServiceForm
    template_name = 'inventory/service_form.html'
    
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
        messages.success(self.request, 'Service created successfully!')
        return reverse_lazy('inventory:service_list')


class ServiceUpdateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, UpdateView):
    """Update a service."""
    model = Service
    form_class = ServiceForm
    template_name = 'inventory/service_form.html'
    
    def get_queryset(self):
        return Service.objects.filter(
            organization=self.request.organization,
            branch=self.request.branch
        )
    
    def get_success_url(self):
        messages.success(self.request, 'Service updated successfully!')
        return reverse_lazy('inventory:service_list')


class ServiceDeleteView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, DeleteView):
    """Delete a service."""
    model = Service
    template_name = 'inventory/service_confirm_delete.html'
    context_object_name = 'service'
    
    def get_queryset(self):
        return Service.objects.filter(
            organization=self.request.organization,
            branch=self.request.branch
        )
    
    def get_success_url(self):
        messages.success(self.request, 'Service deleted successfully!')
        return reverse_lazy('inventory:service_list')


# Stock Movement Views
class StockMovementListView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, ListView):
    """List all stock movements."""
    model = StockMovement
    template_name = 'inventory/stockmovement_list.html'
    context_object_name = 'movements'
    paginate_by = 20
    
    def get_queryset(self):
        return StockMovement.objects.filter(
            organization=self.request.organization,
            branch=self.request.branch
        ).order_by('-date')


class StockMovementDetailView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, DetailView):
    """Stock movement detail view."""
    model = StockMovement
    template_name = 'inventory/stockmovement_detail.html'
    context_object_name = 'movement'
    
    def get_queryset(self):
        return StockMovement.objects.filter(
            organization=self.request.organization,
            branch=self.request.branch
        )


# Stock Transfer Views
class StockTransferListView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, ListView):
    """List all stock transfers."""
    model = StockTransfer
    template_name = 'inventory/stocktransfer_list.html'
    context_object_name = 'transfers'
    paginate_by = 20
    
    def get_queryset(self):
        return StockTransfer.objects.filter(
            organization=self.request.organization
        ).order_by('-transfer_date')


class StockTransferDetailView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, DetailView):
    """Stock transfer detail view."""
    model = StockTransfer
    template_name = 'inventory/stocktransfer_detail.html'
    context_object_name = 'transfer'
    
    def get_queryset(self):
        return StockTransfer.objects.filter(
            organization=self.request.organization
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = StockTransferItem.objects.filter(
            transfer=self.object
        )
        return context


# StockTransferForm not defined, commenting out for now
# class StockTransferCreateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, CreateView):
#     """Create a new stock transfer."""
#     model = StockTransfer
#     form_class = StockTransferForm
#     template_name = 'inventory/stocktransfer_form.html'
#     
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['organization'] = self.request.organization
#         kwargs['branch'] = self.request.branch
#         return kwargs
#     
#     def form_valid(self, form):
#         form.instance.organization = self.request.organization
#         form.instance.from_branch = self.request.branch
#         return super().form_valid(form)
#     
#     def get_success_url(self):
#         messages.success(self.request, 'Stock transfer created successfully!')
#         return reverse_lazy('inventory:stocktransfer_detail', kwargs={'pk': self.object.pk})


# Stock Adjustment Views
class StockAdjustmentListView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, ListView):
    """List all stock adjustments."""
    model = StockAdjustment
    template_name = 'inventory/stockadjustment_list.html'
    context_object_name = 'adjustments'
    paginate_by = 20
    
    def get_queryset(self):
        return StockAdjustment.objects.filter(
            organization=self.request.organization,
            branch=self.request.branch
        ).order_by('-adjustment_date')


class StockAdjustmentDetailView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, DetailView):
    """Stock adjustment detail view."""
    model = StockAdjustment
    template_name = 'inventory/stockadjustment_detail.html'
    context_object_name = 'adjustment'
    
    def get_queryset(self):
        return StockAdjustment.objects.filter(
            organization=self.request.organization,
            branch=self.request.branch
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = StockAdjustmentItem.objects.filter(
            adjustment=self.object
        )
        return context


# StockAdjustmentForm not defined, commenting out for now
# class StockAdjustmentCreateView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, CreateView):
#     """Create a new stock adjustment."""
#     model = StockAdjustment
#     form_class = StockAdjustmentForm
#     template_name = 'inventory/stockadjustment_form.html'
#     
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['organization'] = self.request.organization
#         kwargs['branch'] = self.request.branch
#         return kwargs
#     
#     def form_valid(self, form):
#         form.instance.organization = self.request.organization
#         form.instance.branch = self.request.branch
#         return super().form_valid(form)
#     
#     def get_success_url(self):
#         messages.success(self.request, 'Stock adjustment created successfully!')
#         return reverse_lazy('inventory:stockadjustment_detail', kwargs={'pk': self.object.pk})
