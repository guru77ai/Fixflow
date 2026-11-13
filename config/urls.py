"""
URL configuration for FixSoftRepair Pro project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


# Non-localized URLs (API, admin, auth, static/media)
# These should NOT be wrapped in i18n_patterns
urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # JWT Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Language switch (this endpoint itself is not localized)
    path('i18n/setlang/', set_language, name='set_language'),
]

# API v1 endpoints - mount API routers for business modules
# For system modules that don't have api_urls.py, use their urls.py which contain API endpoints
urlpatterns += [
    path('api/v1/', include([
        # Core and system modules (using urls.py as they contain API endpoints)
        path('accounts/', include('apps.accounts.urls')),
        path('organizations/', include('apps.organizations.urls')),
        path('branches/', include('apps.branches.urls')),
        path('licensing/', include('apps.licensing.urls')),
        path('audit-logs/', include('apps.audit_logs.urls')),
        path('settings/', include('apps.settings.urls')),
        path('dashboard/', include('apps.dashboard.urls')),
        path('notifications/', include('apps.notifications.urls')),
        path('backups/', include('apps.backups.urls')),
        path('reports/', include('apps.reports.urls')),
        path('documents/', include('apps.documents.urls')),
        path('barcode/', include('apps.barcode.urls')),
        path('zakat/', include('apps.zakat.urls')),
        
        # Business modules (using api_urls.py which contain DRF routers)
        path('crm/', include('apps.crm.api_urls')),
        path('repair/', include('apps.repair.api_urls')),
        path('inventory/', include('apps.inventory.api_urls')),
        path('suppliers/', include('apps.suppliers.api_urls')),
        path('pos/', include('apps.pos.api_urls')),
        path('financial/', include('apps.financial.api_urls')),
        path('accounting/', include('apps.accounting.api_urls')),
        path('hr/', include('apps.hr.api_urls')),
    ])),
]

# Django auth URLs (not localized)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

# Localized frontend URLs
# These will be wrapped in i18n_patterns below
frontend_urlpatterns = [
    # Main application frontend
    path('', include('apps.dashboard.urls_frontend')),
    
    # Business module frontend URLs
    path('crm/', include('apps.crm.urls')),
    path('repair/', include('apps.repair.urls')),
    path('inventory/', include('apps.inventory.urls')),
    path('suppliers/', include('apps.suppliers.urls')),
    path('pos/', include('apps.pos.urls')),
    path('financial/', include('apps.financial.urls')),
    path('accounting/', include('apps.accounting.urls')),
    path('hr/', include('apps.hr.urls')),
]

# Wrap frontend URLs with i18n patterns
urlpatterns += i18n_patterns(*frontend_urlpatterns)

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
