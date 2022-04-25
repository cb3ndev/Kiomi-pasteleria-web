from .base import *
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['kiomi-pasteleria.herokuapp.com']

# host allowed
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
# Correr "heroku pg:info" en el CLI para saber mas información de la base de datos en heroku

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd42nnt50q34e59',
        'USER': 'ctxvpaouspjhbx',
        'PASSWORD': 'f9741190af4c0fe52161b39363aa63d57b94b635112c879394fa9e12db5b82ed',
        'HOST': 'ec2-3-218-171-44.compute-1.amazonaws.com',
        'PORT': 5432,
    }
}
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

STATICFILES_DIRS = (BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
