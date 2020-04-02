"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import logging
import os
import platform
import socket
import warnings

from django.contrib.messages import constants as messages
from django.core.exceptions import ImproperlyConfigured

#
# Environment setup
#

VERSION = '1.0.0-dev'

# Hostname
HOSTNAME = platform.node()

# Set the base directory two levels up
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Validate Python version
if platform.python_version_tuple() < ('3', '5'):
    raise RuntimeError(
        "Base project requires Python 3.5 or higher (current: Python {})".format(platform.python_version)
    )
elif platform.python_version_tuple() < ('3', '6'):
    warnings.warn(
        "Python 3.6 or higher will be required starting with Base v1.0.0 (current: Python {})".format(
            platform.python_version()
        )
    )


# 
# Configuraion import
#

try:
    from config import configuration
except ImportError:
    raise ImproperlyConfigured(
        "Configuration file is not preset. Pleade defile config/configuration.py per the documentation."
    )

# Enforce required configuration parameters
for parameter in ['ALLOWED_HOSTS', 'DATABASE', 'SECRET_KEY']:
    if not hasattr(configuration, parameter):
        raise ImproperlyConfigured(
            "Required parameter {} is missing from configuration.py.".format(parameter)
        )

# Default SQLite Database configuration
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Set required parameters
ALLOWED_HOSTS = getattr(configuration, 'ALLOWED_HOSTS')
DATABASE = getattr(configuration, 'DATABASE', DATABASES)
SECRET_KEY = getattr(configuration, 'SECRET_KEY')

# Set optional parameters
BASE_PATH = getattr(configuration, 'BASE_PATH', '')
if BASE_PATH:
    BASE_PATH = BASE_PATH.strip('/') + '/' # Enforce trailing slash only
DEBUG = getattr(configuration, 'DEBUG', False)
EMAIL = getattr(configuration, 'EMAIL', {})
LOGGING = getattr(configuration, 'LOGGING', {})
LOGING_REQUIRED = getattr(configuration, 'LOGING_REQUIRED', False)
LOGING_TIMEOUT = getattr(configuration, 'LOGING_TIMEOUT', None)
MEDIA_ROOT = getattr(configuration, 'MEDIA_ROOT', os.path.join(BASE_DIR, 'media')).rstrip('/')
PAGINATE_COUNT = getattr(configuration, 'PAGINATION_COUNT', 50)
SESSION_FILE_PATH = getattr(configuration, 'SESSION_FILE_PATH', None)
SHORT_DATE_FORMAT = getattr(configuration, 'SHORT_DATE_FORMAT', 'Y-m-d H:i')
SHORT_DATETIME_FORMAT = getattr(configuration, 'SHORT_DATETIME_FORMAT', 'H:i:s')
TIME_FORMAT = getattr(configuration, 'TIME_FORMAT', 'g:i a')
TIME_ZONE = getattr(configuration, 'TIME_ZONE', 'UTC')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

#
# Session
#

if LOGING_TIMEOUT is not None:
    # Django default is 1209600 seconds (14 days)
    SESSION_COOKIE_AGE = LOGING_TIMEOUT
if SESSION_FILE_PATH is not None:
    SESSION_ENGINE = 'django.contrib.session.backends.file'

#
# Email
#

# For gmail
EMAIL_USER_TLS = EMAIL.get('TLS', False)
EMAIL_HOST = EMAIL.get('SERVER')
EMAIL_PORT = EMAIL.get('PORT', 25)
EMAIL_HOST_USER = EMAIL.get('USERNAME')
EMAIL_HOST_PASSWORD = EMAIL.get('PASSWORD')
EMAIL_TIMEOUT = EMAIL.get('TIMEOUT', 10)
SERVER_EMAIL = EMAIL.get('FROM_EMAIL')
EMAIL_SUBJECT_PREFIX = '[Base] '
EMAIL_BACKENDS = EMAIL.get('BACKENDS', False)

if EMAIL_BACKENDS:
    EMAIL_BACKENDS = 'django.core.mail.backends.console.EmailBackend'

#
# Django
#

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_extensions',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES_DIR = BASE_DIR + '/templates'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# Internationalization
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True

WSGI_APPLICATION = 'config.wsgi.application'

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = BASE_DIR + '/static'
STATIC_URL = '/{}static/'.format(BASE_PATH)
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "..", 'resources/static'),
)

# Media
MEDIA_URL = '/{}media/'.format(BASE_PATH)

# Messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# Authentication URLs
LOGIN_URL = '/{}login/'.format(BASE_PATH)

CSRF_TRUSTED_ORIGINS = ALLOWED_HOSTS

REST_FRAMEWORK_VERSION = VERSION[0:3] # User major.minior as API version
REST_FRAMEWORK = {
    'ALLOWED_VERSIONS': [REST_FRAMEWORK_VERSION],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 'netbox.api.TockenAuthentication',
    ),
    # 'DEFAULT_FILTER_BACKENDS': (
    #     'django_filters.resut_framewirl.DjangofilterBackend',
    # ),
    # 'DEFAULT_PAGINATION_CLASS': 'netbox.api.OptionalLimitOffsetPagination',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        # 'netbox.api.TokenPermissions',
    ),
    # 'DEFAULT_RENDERED_CLASSES': (
        # 'rest_framework.renders.JSONRender',
        # 'netbox.api.FormlessBrowsableAPIRenderer',
    # ),
    'DEFAULT_VERSION': REST_FRAMEWORK_VERSION,
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    # 'PAGE_SIZE': PAGINATE_COUNT,
    # 'VIEW_NAME_FUNCTION': 'netbox.api.get_view_name'
}