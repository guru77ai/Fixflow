"""
Views for HR module
"""
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import *
from .forms import *
from apps.core.mixins import OrganizationContextMixin, BranchContextMixin


class DashboardView(LoginRequiredMixin, OrganizationContextMixin, BranchContextMixin, ListView):
    template_name = 'hr/dashboard.html'
    
    def get_queryset(self):
        return []
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'hr'
        return context
