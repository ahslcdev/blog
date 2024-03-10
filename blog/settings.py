import os
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
env = environ.Env()

SECRET_KEY = env("SECRET_KEY")

DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

THIRD_PACKAGES = [
    'drf_yasg',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'drf_standardized_errors',
    'django_filters',
]

CUSTOM_APPS = [
    'apps.core',
    'apps.autenticacao',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
] + THIRD_PACKAGES + CUSTOM_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['apps/templates'],
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

WSGI_APPLICATION = 'blog.wsgi.application'

DATABASES = {
    env('DB_ALIAS'): {
        'ENGINE': env('DB_ENGINE'),
        'NAME': env('DB_NAME'),
        'USER': env("DB_USER"),
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': env("DB_HOST"),
    },
}

# Cache
CACHES = {
    'default': {
        'BACKEND': env('ALIAS_CACHE_DB'),
        'LOCATION': env('URL_CACHE'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient'
        },
        'KEY_PREFIX': 'django_orm'
    }
}

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

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

""" Configurações do RESTFRAMEWORK """
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.DjangoModelPermissions',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler"
}

DRF_STANDARDIZED_ERRORS = {
    "EXCEPTION_FORMATTER_CLASS": "apps.utils.CustomExceptionFormatter"
}

CORS_ALLOW_CREDENTIALS = False
# CORS_ORIGIN_WHITELIST = env.list("FRONT_URLS")
# CSRF_TRUSTED_ORIGINS = env.list("FRONT_URLS")
# CORS_ALLOW_METHODS = (
#     "DELETE",
#     "GET",
#     # "OPTIONS",
#     "PATCH",
#     "POST",
#     "PUT",
# )
# CORS_ALLOW_HEADERS = "*"
# CORS_ALLOWED_ORIGINS = env.list("FRONT_URLS")
