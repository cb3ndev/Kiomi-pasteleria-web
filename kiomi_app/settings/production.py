from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['kiomi-test-v1.herokuapp.com']

# host allowed
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd9198mrdp4nqu3',
				'USER': 'knodbuhkvablcf',
				'PASSWORD': 'f7bd54050a9b1a5701ffc32db4362e0c8099096e4c85e4c07b812e8bd7833e69',
				'HOST': 'ec2-3-222-235-188.compute-1.amazonaws.com',
				'PORT': 5432,
    }
}

STATICFILES_DIRS = (BASE_DIR, 'static')
STATIC_ROOT = os.path.join(BASE_DIR, 'static_cdn')

