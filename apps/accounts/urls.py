from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/settings/', views.profile_settings, name='profile_settings'),
    path('profile/security/', views.profile_security, name='profile_security'),
    
    # Admin URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/users/<uuid:uid>/edit/', views.admin_user_edit, name='admin_user_edit'),
    path('admin/users/<uuid:uid>/delete/', views.admin_user_delete, name='admin_user_delete'),
    path('admin/users/<uuid:uid>/ban/', views.admin_ban_user, name='admin_ban_user'),
    path('admin/messages/', views.admin_messages, name='admin_messages'),
    path('admin/messages/send/', views.admin_send_message, name='admin_send_message'),
    path('admin/messages/<int:message_id>/', views.admin_message_detail, name='admin_message_detail'),
]