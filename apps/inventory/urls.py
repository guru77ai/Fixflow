"""
URLs for Inventory module frontend views
"""
from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # Warehouse URLs
    path('warehouses/', views.WarehouseListView.as_view(), name='warehouse_list'),
    path('warehouses/create/', views.WarehouseCreateView.as_view(), name='warehouse_create'),
    path('warehouses/<uuid:pk>/', views.WarehouseDetailView.as_view(), name='warehouse_detail'),
    path('warehouses/<uuid:pk>/edit/', views.WarehouseUpdateView.as_view(), name='warehouse_update'),
    path('warehouses/<uuid:pk>/delete/', views.WarehouseDeleteView.as_view(), name='warehouse_delete'),
    
    # Product Category URLs
    path('categories/', views.ProductCategoryListView.as_view(), name='productcategory_list'),
    path('categories/create/', views.ProductCategoryCreateView.as_view(), name='productcategory_create'),
    path('categories/<uuid:pk>/edit/', views.ProductCategoryUpdateView.as_view(), name='productcategory_update'),
    path('categories/<uuid:pk>/delete/', views.ProductCategoryDeleteView.as_view(), name='productcategory_delete'),
    
    # Product Brand URLs
    path('brands/', views.ProductBrandListView.as_view(), name='productbrand_list'),
    path('brands/create/', views.ProductBrandCreateView.as_view(), name='productbrand_create'),
    path('brands/<uuid:pk>/edit/', views.ProductBrandUpdateView.as_view(), name='productbrand_update'),
    path('brands/<uuid:pk>/delete/', views.ProductBrandDeleteView.as_view(), name='productbrand_delete'),
    
    # Unit of Measure URLs
    path('units/', views.UnitOfMeasureListView.as_view(), name='unitofmeasure_list'),
    path('units/create/', views.UnitOfMeasureCreateView.as_view(), name='unitofmeasure_create'),
    path('units/<uuid:pk>/edit/', views.UnitOfMeasureUpdateView.as_view(), name='unitofmeasure_update'),
    path('units/<uuid:pk>/delete/', views.UnitOfMeasureDeleteView.as_view(), name='unitofmeasure_delete'),
    
    # Product URLs
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<uuid:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<uuid:pk>/edit/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<uuid:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    
    # Service Category URLs
    path('service-categories/', views.ServiceCategoryListView.as_view(), name='servicecategory_list'),
    path('service-categories/create/', views.ServiceCategoryCreateView.as_view(), name='servicecategory_create'),
    path('service-categories/<uuid:pk>/edit/', views.ServiceCategoryUpdateView.as_view(), name='servicecategory_update'),
    path('service-categories/<uuid:pk>/delete/', views.ServiceCategoryDeleteView.as_view(), name='servicecategory_delete'),
    
    # Service URLs
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/create/', views.ServiceCreateView.as_view(), name='service_create'),
    path('services/<uuid:pk>/edit/', views.ServiceUpdateView.as_view(), name='service_update'),
    path('services/<uuid:pk>/delete/', views.ServiceDeleteView.as_view(), name='service_delete'),
    
    # Stock Movement URLs
    path('stock-movements/', views.StockMovementListView.as_view(), name='stockmovement_list'),
    path('stock-movements/<uuid:pk>/', views.StockMovementDetailView.as_view(), name='stockmovement_detail'),
    
    # Stock Transfer URLs
    path('stock-transfers/', views.StockTransferListView.as_view(), name='stocktransfer_list'),
    # path('stock-transfers/create/', views.StockTransferCreateView.as_view(), name='stocktransfer_create'),
    path('stock-transfers/<uuid:pk>/', views.StockTransferDetailView.as_view(), name='stocktransfer_detail'),
    
    # Stock Adjustment URLs
    path('stock-adjustments/', views.StockAdjustmentListView.as_view(), name='stockadjustment_list'),
    # path('stock-adjustments/create/', views.StockAdjustmentCreateView.as_view(), name='stockadjustment_create'),
    path('stock-adjustments/<uuid:pk>/', views.StockAdjustmentDetailView.as_view(), name='stockadjustment_detail'),
]
