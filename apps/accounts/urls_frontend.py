"""
Frontend URLs for the accounts application.
"""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('password-reset/done/', views.password_reset_done_view, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete_view, name='password_reset_complete'),
    
    # User profile and settings
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_view, name='profile_edit'),
    path('account/settings/', views.settings_view, name='settings'),
    path('account/password/change/', views.password_reset_view, name='password_change'),
    
    # User management
    path('users/', views.users_view, name='user_list'),
    path('users/create/', views.users_view, name='user_form'),
]
