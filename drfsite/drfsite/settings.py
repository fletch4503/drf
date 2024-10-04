"""
Django settings for drfsite project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-$7keb2q!=rvz1y4+^2vn@3($n%r%&=50ixzzl#$4=359j7fedt"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django_auth_exchange",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'women.apps.WomenConfig',
    'ews_list.apps.EwsListConfig',
    'rest_framework',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "drfsite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "drfsite.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Documentation: https://django-auth-exchange.readthedocs.io
# Auth Exchange is a reusable Django app that allows you to authenticate users against an Exchange/Office365
# server (using exchangelib).
AUTHENTICATION_BACKENDS = [
    'django_auth_exchange.backends.ExchangeAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Configure at least one domain
AUTH_EXCHANGE_DOMAIN_SERVERS = {
    'example.org': 'autodiscover',
}

# AUTH_EXCHANGE_CREATE_UNKNOWN_USER (default: True)
#   - Determines if users should be created if they are not found in the local database.
# AUTH_EXCHANGE_DEFAULT_DOMAIN (default: 'example.com')
#   - If only a username is provided, this is the default domain that will be associated.
# AUTH_EXCHANGE_ALLOWED_FORMATS (default: ['email', 'netbios', 'username'])
#   - This specifies which formats are allowed as the username (email means someuser@example.com,
#       netbios means EXAMPLE\someuser, and username means someuser).
# AUTH_EXCHANGE_DOMAIN_SERVERS (default: {})
#   - This specifies the domains which are allowed to authenticate and
#       the server that should be used for authentication (or 'autodiscover').
#       Hint: Office365 uses the server outlook.office365.com.
# AUTH_EXCHANGE_DOMAIN_USER_PROPERTIES (default: {})
#   - This specifies the settings we should apply to a user when they are added to the local database for each domain
#   (e.g., to make all example.com users superusers, do: {'example.com': {'is_staff': True, 'is_superuser': True}}).
# AUTH_EXCHANGE_NETBIOS_TO_DOMAIN_MAP (default: {}) - This specifies a mapping from NETBIOS names to domain names.

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
