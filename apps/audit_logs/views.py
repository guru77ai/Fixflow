"""
Views for the audit_logs application.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import AuditLog, FinancialAuditLog
from .services import AuditLogService
from .selectors import AuditLogSelector


# Frontend Views

@login_required
def audit_log_list_view(request):
    """
    List all audit logs.
    """
    selector = AuditLogSelector(request)
    audit_logs = selector.get_audit_logs()
    
    context = {
        'page_title': _('Audit Logs'),
        'audit_logs': audit_logs,
    }
    
    return render(request, 'audit_logs/list.html', context)


# API Views

class AuditLogListAPIView(APIView):
    """
    API endpoint for listing audit logs.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        selector = AuditLogSelector(request)
        audit_logs = selector.get_audit_logs()
        return Response(audit_logs)


class AuditLogDetailAPIView(APIView):
    """
    API endpoint for audit log details.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        selector = AuditLogSelector(request)
        audit_log = selector.get_audit_log(pk)
        if audit_log:
            return Response(audit_log)
        return Response({'error': 'Audit log not found'}, status=status.HTTP_404_NOT_FOUND)
