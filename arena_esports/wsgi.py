"""
WSGI config for arena_esports project.
It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arena_esports.settings')

application = get_wsgi_application()

# Vercel deployment support
app = application