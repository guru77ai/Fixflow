"""
Views for the organizations application.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Organization, OrganizationMembership
from .forms import OrganizationForm, OrganizationMembershipForm
from .services import OrganizationService
from .selectors import OrganizationSelector


# Frontend Views

@login_required
def organization_list_view(request):
    """
    List all organizations.
    """
    selector = OrganizationSelector(request)
    organizations = selector.get_organizations()
    
    context = {
        'page_title': _('Organizations'),
        'organizations': organizations,
    }
    
    return render(request, 'organizations/list.html', context)


@login_required
def organization_create_view(request):
    """
    Create a new organization.
    """
    if request.method == 'POST':
        form = OrganizationForm(request.POST, request.FILES)
        if form.is_valid():
            organization = form.save()
            
            # Create membership for current user as owner
            OrganizationMembership.objects.create(
                organization=organization,
                user=request.user,
                is_owner=True,
                is_admin=True,
                can_manage_users=True,
                can_manage_settings=True,
                can_access_all_branches=True
            )
            
            # Set as current organization
            request.session['organization_id'] = str(organization.id)
            
            messages.success(request, _('Organization created successfully.'))
            return redirect('organizations:list')
    else:
        form = OrganizationForm()
    
    context = {
        'page_title': _('Create Organization'),
        'form': form,
    }
    
    return render(request, 'organizations/create.html', context)


@login_required
def organization_detail_view(request, pk):
    """
    View organization details.
    """
    organization = get_object_or_404(Organization, pk=pk)
    selector = OrganizationSelector(request)
    organization_data = selector.get_organization(organization.id)
    
    context = {
        'page_title': organization.name,
        'organization': organization_data,
    }
    
    return render(request, 'organizations/detail.html', context)


@login_required
def organization_edit_view(request, pk):
    """
    Edit an organization.
    """
    organization = get_object_or_404(Organization, pk=pk)
    
    if request.method == 'POST':
        form = OrganizationForm(request.POST, request.FILES, instance=organization)
        if form.is_valid():
            form.save()
            messages.success(request, _('Organization updated successfully.'))
            return redirect('organizations:detail', pk=organization.id)
    else:
        form = OrganizationForm(instance=organization)
    
    context = {
        'page_title': _('Edit Organization'),
        'organization': organization,
        'form': form,
    }
    
    return render(request, 'organizations/edit.html', context)


@login_required
def organization_delete_view(request, pk):
    """
    Delete an organization.
    """
    organization = get_object_or_404(Organization, pk=pk)
    
    if request.method == 'POST':
        # Check if user can delete this organization
        membership = OrganizationMembership.objects.filter(
            organization=organization,
            user=request.user,
            is_owner=True
        ).exists()
        
        if not membership:
            messages.error(request, _('You do not have permission to delete this organization.'))
            return redirect('organizations:detail', pk=organization.id)
        
        # Soft delete
        organization.is_active = False
        organization.save()
        
        messages.success(request, _('Organization deleted successfully.'))
        return redirect('organizations:list')
    
    context = {
        'page_title': _('Delete Organization'),
        'organization': organization,
    }
    
    return render(request, 'organizations/delete.html', context)


# API Views

class OrganizationListAPIView(APIView):
    """
    API endpoint for listing organizations.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        selector = OrganizationSelector(request)
        organizations = selector.get_organizations()
        return Response(organizations)
    
    def post(self, request):
        service = OrganizationService(request)
        organization = service.create_organization(request.data)
        return Response(organization, status=status.HTTP_201_CREATED)


class OrganizationDetailAPIView(APIView):
    """
    API endpoint for organization details.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        selector = OrganizationSelector(request)
        organization = selector.get_organization(pk)
        if organization:
            return Response(organization)
        return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        service = OrganizationService(request)
        organization = service.update_organization(pk, request.data)
        if organization:
            return Response(organization)
        return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, pk):
        service = OrganizationService(request)
        organization = service.update_organization(pk, request.data, partial=True)
        if organization:
            return Response(organization)
        return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        service = OrganizationService(request)
        success = service.delete_organization(pk)
        if success:
            return Response({'message': 'Organization deleted successfully'})
        return Response({'error': 'Organization not found or cannot be deleted'}, status=status.HTTP_404_NOT_FOUND)
