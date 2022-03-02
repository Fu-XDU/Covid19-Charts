#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import json
import os
import sys
import time


import data


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Covid19Data.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if sys.argv[1] == 'runserver':
        data.getEnv()
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()