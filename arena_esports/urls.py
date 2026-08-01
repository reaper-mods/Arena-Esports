# arena_esports/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.accounts.views import home_view, wallet_view, leaderboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls')),
    path('tournaments/', include('apps.tournaments.urls')),
    path('messages/', include('apps.messaging.urls')),
    
    # Main pages
    path('', home_view, name='home'),
    path('wallet/', wallet_view, name='wallet'),
    path('leaderboard/', leaderboard_view, name='leaderboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)