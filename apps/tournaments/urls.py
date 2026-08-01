from django.urls import path
from . import views

urlpatterns = [
    path('', views.tournament_list, name='tournament_list'),
    path('featured/', views.featured_tournaments, name='featured_tournaments'),
    path('search/', views.search_tournaments, name='search_tournaments'),
    path('<uuid:uid>/', views.tournament_detail, name='tournament_detail'),
    path('<uuid:uid>/register/', views.tournament_register, name='tournament_register'),
    path('<uuid:uid>/unregister/', views.tournament_unregister, name='tournament_unregister'),
    path('<uuid:uid>/participants/', views.tournament_participants, name='tournament_participants'),
    
    # Admin URLs
    path('admin/list/', views.admin_tournaments, name='admin_tournaments'),
    path('admin/create/', views.admin_create_tournament, name='admin_create_tournament'),
    path('admin/<uuid:uid>/edit/', views.admin_edit_tournament, name='admin_edit_tournament'),
    path('admin/<uuid:uid>/delete/', views.admin_delete_tournament, name='admin_delete_tournament'),
    path('admin/<uuid:uid>/results/', views.admin_tournament_results, name='admin_tournament_results'),
]