"""
URLs for Suppliers module frontend views
"""
from django.urls import path
from . import views

app_name = 'suppliers'

urlpatterns = [
    # Supplier Category URLs
    path('categories/', views.SupplierCategoryListView.as_view(), name='suppliercategory_list'),
    path('categories/create/', views.SupplierCategoryCreateView.as_view(), name='suppliercategory_create'),
    path('categories/<uuid:pk>/', views.SupplierCategoryDetailView.as_view(), name='suppliercategory_detail'),
    path('categories/<uuid:pk>/edit/', views.SupplierCategoryUpdateView.as_view(), name='suppliercategory_update'),
    path('categories/<uuid:pk>/delete/', views.SupplierCategoryDeleteView.as_view(), name='suppliercategory_delete'),
    path('categories/form/', views.SupplierCategoryCreateView.as_view(), name='suppliercategory_form'),
    path('categories/form/<uuid:pk>/', views.SupplierCategoryUpdateView.as_view(), name='suppliercategory_form'),
    
    # Supplier URLs
    path('', views.SupplierListView.as_view(), name='supplier_list'),
    path('create/', views.SupplierCreateView.as_view(), name='supplier_create'),
    path('<uuid:pk>/', views.SupplierDetailView.as_view(), name='supplier_detail'),
    path('<uuid:pk>/edit/', views.SupplierUpdateView.as_view(), name='supplier_update'),
    path('<uuid:pk>/delete/', views.SupplierDeleteView.as_view(), name='supplier_delete'),
    
    # Supplier Contact URLs
    path('<uuid:supplier_pk>/contacts/', views.SupplierContactListView.as_view(), name='suppliercontact_list'),
    path('<uuid:supplier_pk>/contacts/create/', views.SupplierContactCreateView.as_view(), name='suppliercontact_create'),
    path('<uuid:supplier_pk>/contacts/<uuid:pk>/', views.SupplierContactDetailView.as_view(), name='suppliercontact_detail'),
    path('<uuid:supplier_pk>/contacts/<uuid:pk>/edit/', views.SupplierContactUpdateView.as_view(), name='suppliercontact_update'),
    path('<uuid:supplier_pk>/contacts/<uuid:pk>/delete/', views.SupplierContactDeleteView.as_view(), name='suppliercontact_delete'),
    path('<uuid:supplier_pk>/contacts/form/', views.SupplierContactCreateView.as_view(), name='suppliercontact_form'),
    path('<uuid:supplier_pk>/contacts/form/<uuid:pk>/', views.SupplierContactUpdateView.as_view(), name='suppliercontact_form'),
    
    # Supplier Document URLs
    path('<uuid:supplier_pk>/documents/', views.SupplierDocumentListView.as_view(), name='supplierdocument_list'),
    path('<uuid:supplier_pk>/documents/create/', views.SupplierDocumentCreateView.as_view(), name='supplierdocument_create'),
    path('<uuid:supplier_pk>/documents/<uuid:pk>/', views.SupplierDocumentDetailView.as_view(), name='supplierdocument_detail'),
    path('<uuid:supplier_pk>/documents/<uuid:pk>/delete/', views.SupplierDocumentDeleteView.as_view(), name='supplierdocument_delete'),
    path('<uuid:supplier_pk>/documents/form/', views.SupplierDocumentCreateView.as_view(), name='supplierdocument_form'),
    path('<uuid:supplier_pk>/documents/form/<uuid:pk>/', views.SupplierDocumentUpdateView.as_view(), name='supplierdocument_form'),
]
