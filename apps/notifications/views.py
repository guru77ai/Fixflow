"""
Views for the notifications application.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Notification, NotificationTemplate, NotificationPreference
from .services import NotificationService
from .selectors import NotificationSelector


# Frontend Views

@login_required
def notification_list_view(request):
    """
    List all notifications.
    """
    selector = NotificationSelector(request)
    notifications = selector.get_notifications()
    
    context = {
        'page_title': _('Notifications'),
        'notifications': notifications,
    }
    
    return render(request, 'notifications/list.html', context)


@login_required
def notification_detail_view(request, pk):
    """
    View notification details.
    """
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    
    # Mark as read
    notification.mark_as_read()
    
    context = {
        'page_title': _('Notification Details'),
        'notification': notification,
    }
    
    return render(request, 'notifications/detail.html', context)


# API Views

class NotificationListAPIView(APIView):
    """
    API endpoint for listing notifications.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        selector = NotificationSelector(request)
        notifications = selector.get_notifications()
        return Response(notifications)


class NotificationDetailAPIView(APIView):
    """
    API endpoint for notification details.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        selector = NotificationSelector(request)
        notification = selector.get_notification(pk)
        if notification:
            return Response(notification)
        return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        service = NotificationService(request)
        success = service.delete_notification(pk)
        if success:
            return Response({'message': 'Notification deleted successfully'})
        return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)


class NotificationMarkReadAPIView(APIView):
    """
    API endpoint for marking notifications as read.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        service = NotificationService(request)
        notification = service.mark_notification_as_read(pk)
        if notification:
            return Response({'message': 'Notification marked as read'})
        return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)


class NotificationMarkAllReadAPIView(APIView):
    """
    API endpoint for marking all notifications as read.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        service = NotificationService(request)
        count = service.mark_all_notifications_as_read()
        return Response({'message': f'{count} notifications marked as read'})
