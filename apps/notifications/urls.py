"""
URLs for the notifications application.
"""
from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # API URLs
    path('', views.NotificationListAPIView.as_view(), name='api_list'),
    path('<uuid:pk>/', views.NotificationDetailAPIView.as_view(), name='api_detail'),
    path('<uuid:pk>/mark-read/', views.NotificationMarkReadAPIView.as_view(), name='api_mark_read'),
    path('mark-all-read/', views.NotificationMarkAllReadAPIView.as_view(), name='api_mark_all_read'),
]
