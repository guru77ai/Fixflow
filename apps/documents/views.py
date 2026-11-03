"""
Views for the documents application.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse, FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .services import DocumentService
from .selectors import DocumentSelector


# Frontend Views

@login_required
def document_list_view(request):
    """
    List all documents.
    """
    selector = DocumentSelector(request)
    documents = selector.get_documents()
    
    context = {
        'page_title': _('Documents'),
        'documents': documents,
    }
    
    return render(request, 'documents/list.html', context)


# API Views

class DocumentListAPIView(APIView):
    """
    API endpoint for listing documents.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        selector = DocumentSelector(request)
        documents = selector.get_documents()
        return Response(documents)


class DocumentDetailAPIView(APIView):
    """
    API endpoint for document details.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        selector = DocumentSelector(request)
        document = selector.get_document(pk)
        if document:
            return Response(document)
        return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
