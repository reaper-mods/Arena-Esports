from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('sent/', views.sent_messages, name='sent_messages'),
    path('<int:message_id>/', views.message_detail, name='message_detail'),
    path('<int:message_id>/read/', views.mark_as_read, name='mark_as_read'),
    path('<int:message_id>/delete/', views.delete_message, name='delete_message'),
    path('compose/', views.compose_message, name='compose_message'),
    path('broadcast/', views.broadcast_message, name='broadcast_message'),
]