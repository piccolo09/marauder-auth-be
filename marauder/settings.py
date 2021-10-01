"""
Generated by 'django-admin startproject' using Django 3.2.7.
"""
from urllib import request
import json
from pathlib import Path
from datetime import timedelta
import os.path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'rest_framework',
    'corsheaders',
    'djoser',
    'accounts'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.RemoteUserBackend',
    'django.contrib.auth.backends.ModelBackend',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# DATABASES['default'] = dj_database_url.parse(
#   config('DATABASE_URL'),conn_max_age=600, ssl_require=True)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


WSGI_APPLICATION = 'marauder.wsgi.application'

ROOT_URLCONF = 'marauder.urls'

AUTH_USER_MODEL = 'accounts.User'


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )

CORS_ORIGIN_ALLOW_ALL = True

# CORS_ORIGIN_WHITELIST = (
#   'http://localhost:8000',
#   'http://localhost:3000',
# )

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSON_CLASSES': (
        # 'rest_framework.permissions.IsAuthticated'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # added simple jwt authclass for jwt token
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

DOMAIN = config('DOMAIN')

SITE_NAME = ('Proto')


DJOSER = {
    "LOGIN_FEILD": "EMAIL",
    "PASSWORD_RESET_CONFIRM_URL": "password/reset/confirm/{uid}/{token}",
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True
}


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.mailtrap.io'

EMAIL_HOST_USER = 'cd6be89df92de8'

EMAIL_HOST_PASSWORD = '2cee8074f35cbf'

EMAIL_PORT = '2525'


COGNITO_AWS_REGION = 'us-east-2'
COGNITO_USER_POOL = 'us-east-2_Z4uNPkF2L'
# Provide this value if `id_token` is used for authentication (it contains 'aud' claim).
# `access_token` doesn't have it, in this case keep the COGNITO_AUDIENCE empty
COGNITO_AUDIENCE = None
COGNITO_POOL_URL = None  # will be set few lines of code later, if configuration provided

rsa_keys = {}


if COGNITO_AWS_REGION and COGNITO_USER_POOL:
    COGNITO_POOL_URL = 'https://cognito-idp.{}.amazonaws.com/{}'.format(
        COGNITO_AWS_REGION, COGNITO_USER_POOL)
    pool_jwks_url = COGNITO_POOL_URL + '/.well-known/jwks.json'
    jwks = json.loads(request.urlopen(pool_jwks_url).read())
    rsa_keys = {key['kid']: json.dumps(key) for key in jwks['keys']}

SIMPLE_JWT = (
    {
        'BLACKLIST_AFTER_ROTATION': False,
        # set simple jwt expiry for jwt token
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=500),
        # set simple jwt expiry for jwt token
        'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
        'SIGNING_KEY': rsa_keys,
        'ALGORITHM': 'RS256',
        'AUDIENCE': COGNITO_AUDIENCE,
        'ISSUER': COGNITO_POOL_URL,
        'AUTH_HEADER_TYPES': ('Bearer',),
    }
)
