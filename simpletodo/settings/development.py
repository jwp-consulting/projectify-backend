from .base import *

SECRET_KEY = "development"

DEBUG = True

#CORS_ALLOWED_ORIGINS = ("http://localhost:3000")
CORS_ORIGIN_ALLOW_ALL = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DATABASE_NAME', default='simpletodo'),
        'USER': config('DATABASE_USER', default='postgres'),
        'PASSWORD': config('DATABASE_PASSWORD', default='postgres'),
        'HOST': config('DATABASE_HOST', default='localhost'),
        'PORT': config('DATABASE_PORT', default=5432)
    }
}