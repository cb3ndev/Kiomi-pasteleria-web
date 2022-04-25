"""
WSGI config for kiomi_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

# from dj_static import Cling #libreria que ya no se usa
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'kiomi_app.settings.local')

application = get_wsgi_application()

# application = Cling(get_wsgi_application()) #libreria que ya no se usa
