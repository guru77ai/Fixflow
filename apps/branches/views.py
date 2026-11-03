"""
Views for the branches application.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Branch, BranchUserAccess
from .forms import BranchForm
from .services import BranchService
from .selectors import BranchSelector


# Frontend Views

@login_required
def branch_list_view(request):
    """
    List all branches.
    """
    selector = BranchSelector(request)
    branches = selector.get_branches()
    
    context = {
        'page_title': _('Branches'),
        'branches': branches,
    }
    
    return render(request, 'branches/list.html', context)


@login_required
def branch_create_view(request):
    """
    Create a new branch.
    """
    if request.method == 'POST':
        form = BranchForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            branch = form.save()
            messages.success(request, _('Branch created successfully.'))
            return redirect('branches:list')
    else:
        form = BranchForm(user=request.user)
    
    context = {
        'page_title': _('Create Branch'),
        'form': form,
    }
    
    return render(request, 'branches/create.html', context)


@login_required
def branch_detail_view(request, pk):
    """
    View branch details.
    """
    branch = get_object_or_404(Branch, pk=pk)
    selector = BranchSelector(request)
    branch_data = selector.get_branch(branch.id)
    
    if not branch_data:
        messages.error(request, _('You do not have access to this branch.'))
        return redirect('branches:list')
    
    context = {
        'page_title': branch.name,
        'branch': branch_data,
    }
    
    return render(request, 'branches/detail.html', context)


@login_required
def branch_edit_view(request, pk):
    """
    Edit a branch.
    """
    branch = get_object_or_404(Branch, pk=pk)
    selector = BranchSelector(request)
    
    if not selector.has_branch_access(branch):
        messages.error(request, _('You do not have access to this branch.'))
        return redirect('branches:list')
    
    if request.method == 'POST':
        form = BranchForm(request.POST, request.FILES, instance=branch, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Branch updated successfully.'))
            return redirect('branches:detail', pk=branch.id)
    else:
        form = BranchForm(instance=branch, user=request.user)
    
    context = {
        'page_title': _('Edit Branch'),
        'branch': branch,
        'form': form,
    }
    
    return render(request, 'branches/edit.html', context)


@login_required
def branch_delete_view(request, pk):
    """
    Delete a branch.
    """
    branch = get_object_or_404(Branch, pk=pk)
    selector = BranchSelector(request)
    
    if not selector.has_branch_access(branch):
        messages.error(request, _('You do not have access to this branch.'))
        return redirect('branches:list')
    
    if request.method == 'POST':
        # Soft delete
        branch.is_active = False
        branch.save()
        messages.success(request, _('Branch deleted successfully.'))
        return redirect('branches:list')
    
    context = {
        'page_title': _('Delete Branch'),
        'branch': branch,
    }
    
    return render(request, 'branches/delete.html', context)


# API Views

class BranchListAPIView(APIView):
    """
    API endpoint for listing branches.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        selector = BranchSelector(request)
        branches = selector.get_branches()
        return Response(branches)
    
    def post(self, request):
        service = BranchService(request)
        branch = service.create_branch(request.data)
        if branch:
            return Response(branch, status=status.HTTP_201_CREATED)
        return Response(
            {'error': 'You do not have permission to create branches in this organization.'},
            status=status.HTTP_403_FORBIDDEN
        )


class BranchDetailAPIView(APIView):
    """
    API endpoint for branch details.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        selector = BranchSelector(request)
        branch = selector.get_branch(pk)
        if branch:
            return Response(branch)
        return Response({'error': 'Branch not found or access denied'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        service = BranchService(request)
        branch = service.update_branch(pk, request.data)
        if branch:
            return Response(branch)
        return Response({'error': 'Branch not found or access denied'}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, pk):
        service = BranchService(request)
        branch = service.update_branch(pk, request.data, partial=True)
        if branch:
            return Response(branch)
        return Response({'error': 'Branch not found or access denied'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        service = BranchService(request)
        success = service.delete_branch(pk)
        if success:
            return Response({'message': 'Branch deleted successfully'})
        return Response({'error': 'Branch not found or access denied'}, status=status.HTTP_404_NOT_FOUND)
