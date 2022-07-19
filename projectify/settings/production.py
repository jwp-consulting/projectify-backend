"""Production settings."""
import os
import ssl

# flake8: noqa: F401, F403
from .base import *


# Redis URL
# Heroku unsets REDIS_TLS_URL when migrating to premium redis
if "REDIS_TLS_URL" not in os.environ:
    REDIS_TLS_URL = os.environ["REDIS_URL"]
else:
    REDIS_TLS_URL = os.environ["REDIS_TLS_URL"]

SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")

# Want forever-cacheable files and compression support? Just add this to your settings.py:
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

FRONTEND_URL = os.environ["FRONTEND_URL"]

ANYMAIL = {
    "MAILGUN_API_KEY": os.environ["MAILGUN_API_KEY"],
    "MAILGUN_SENDER_DOMAIN": os.environ["MAILGUN_DOMAIN"],
}
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"

# Celery
CELERY_BROKER_URL = REDIS_TLS_URL

CORS_ALLOWED_ORIGINS = (
    "https://www.projectifyapp.com",
    "https://staging.projectifyapp.com",
    "https://testbed.projectifyapp.com",
    "http://localhost:3000",
)
CORS_ALLOWED_ORIGIN_REGEXES = (
    r"^https://deploy-preview-\d+--projectifyapp.netlify.app$",
    r"^https://.+--projectifyapp-staging.netlify.app$",
)

CSRF_TRUSTED_ORIGINS = (
    "https://*.netlify.app",
    "https://www.projectifyapp.com",
    "https://staging.projectifyapp.com",
    "https://testbed.projectifyapp.com",
    "http://localhost:3000",
)

# GraphQL
GRAPHIQL_ENABLE = False

# Cloudinary
DEFAULT_FILE_STORAGE = MEDIA_CLOUDINARY_STORAGE

# Disable CSRF protection
csrf_middleware = "django.middleware.csrf.CsrfViewMiddleware"
if "DISABLE_CSRF_PROTECTION" in os.environ:
    csrf_middleware_index = MIDDLEWARE.index(csrf_middleware)
    MIDDLEWARE[
        csrf_middleware_index
    ] = "projectify.middleware.DisableCSRFMiddleware"

CSRF_COOKIE_DOMAIN = ".projectifyapp.com"


# Stripe
STRIPE_PUBLISHABLE_KEY = os.environ["STRIPE_PUBLISHABLE_KEY"]
STRIPE_SECRET_KEY = os.environ["STRIPE_SECRET_KEY"]
STRIPE_PRICE_OBJECT = os.environ["STRIPE_PRICE_OBJECT"]
STRIPE_ENDPOINT_SECRET = os.environ["STRIPE_ENDPOINT_SECRET"]
