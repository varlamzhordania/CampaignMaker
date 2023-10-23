#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from core.settings.settings import DEBUG


def main():
    """Run administrative tasks."""
    if DEBUG:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
        print("Manage: Django loaded up in setting mode : Development")
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.production')
        print("Manage: Django loaded up in setting mode : Production")

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
