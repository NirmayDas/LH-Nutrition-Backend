"""
WSGI config for ScreenScrapeDB project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ScreenScrapeDB.settings')

application = get_wsgi_application()

# Import the function from views.py
from playground.views import run_scraping_task  # Replace 'your_app_name' with the actual app name

# Run the entire views.py script via the function
run_scraping_task()
