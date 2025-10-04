"""
WSGI config for pola_hidup_tracker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from django.core.wsgi import get_wsgi_application

# Use production settings by default, fall back to development
settings_module = 'pola_hidup_tracker.production_settings' if os.environ.get('DEBUG', 'False') == 'False' else 'pola_hidup_tracker.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
