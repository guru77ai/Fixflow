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


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # JWT Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Language switch
    path('i18n/setlang/', set_language, name='set_language'),
]

# API v1 endpoints
urlpatterns += [
    path('api/v1/', include([
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
        path('crm/', include('apps.crm.urls')),
        path('repair/', include('apps.repair.urls')),
        path('inventory/', include('apps.inventory.urls')),
        path('suppliers/', include('apps.suppliers.urls')),
        path('pos/', include('apps.pos.urls')),
    ])),
]

# Frontend URLs for new modules
urlpatterns += [
    path('crm/', include('apps.crm.urls')),
    path('repair/', include('apps.repair.urls')),
    path('inventory/', include('apps.inventory.urls')),
    path('suppliers/', include('apps.suppliers.urls')),
    path('pos/', include('apps.pos.urls')),
]

# Frontend URLs
urlpatterns += [
    # Authentication
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Main application
    path('', include('apps.dashboard.urls_frontend')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Use i18n patterns for language-specific URLs
urlpatterns = i18n_patterns(*urlpatterns)
