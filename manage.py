#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv(override=True)
import sys


def main():
    """
    Main function to run Django management commands.
    Automatically selects settings file based on ENV variable:
    - local: for local development
    - development: for dev server
    - stage: for staging environment
    - production: for production server
    """
    ENV = os.getenv("ENV")
    if ENV == "local":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.local')
    elif ENV == "development":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.development')
    elif ENV == "stage":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.stage')
    elif ENV == "production":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.production')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
