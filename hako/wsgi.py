"""
WSGI config for hako project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import threading
import time

import requests
from django.core.wsgi import get_wsgi_application

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hako.settings')

application = get_wsgi_application()


def awake():
    while True:
        print(f'awake: access to {settings.HOSTNAME}')
        try:
            requests.get(settings.HOSTNAME)
        except Exception as e:
            print('error:', e)
        time.sleep(600)  # 10 min


t = threading.Thread(target=awake)
t.start()
