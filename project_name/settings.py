"""
Django settings for project_name project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import django_heroku
from decouple import config
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/
## SECURITY WARNING: keep the secret key used in production secret!
## SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('PYTHON_ENV', default='production') == 'development'  # need to make sure this works
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = [
	'event-horizon-jp.herokuapp.com/',
	'event-horizon-test.herokuapp.com/',
	'localhost',
	'eventhorizon.vip/',
	'localhost',
	'localhost/',
	'127.0.0.1',
	'127.0.0.1/',
]

CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_NAME = 'XSRF-TOKEN'

#CORS_ALLOW_ALL_ORIGINS = True  # dangerous, want to restrict origins that can make cross-origin requests
CORS_ALLOWED_ORIGINS = (
	'https://event-horizon-jp.herokuapp.com',
	'https://event-horizon-test.herokuapp.com',
	'http://eventhorizon.vip',
	'https://eventhorizon.vip',
)
if config('PYTHON_ENV', default='production') == 'development':
	CORS_ALLOWED_ORIGINS += (
		'http://127.0.0.1:8080',
		'http://127.0.0.1:8000',
		'http://localhost:8080',
		'http://localhost:8000',
	)
CSRF_TRUSTED_ORIGINS = (
	'https://event-horizon-jp.herokuapp.com',
	'https://event-horizon-test.herokuapp.com',
	'http://eventhorizon.vip',
	'https://eventhorizon.vip',
)
if config('PYTHON_ENV', default='production') == 'development':
	CSRF_TRUSTED_ORIGINS += (
		'http://127.0.0.1:8080',
		'http://127.0.0.1:8000',
		'http://localhost:8080',
		'http://localhost:8000',
	)

# 'Strict': prevents the cookie from being sent by the browser to the target site in all cross-site browsing context, even when following a regular link
# 'Lax': maintain user’s logged-in session after the user arrives from an external link
# 'None': the session cookie will be sent with all same-site and cross-site requests
SESSION_COOKIE_SAMESITE = 'Strict'

#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = 'smtp-mail.outlook.com'
#EMAIL_USE_TLS = True
#EMAIL_PORT = 25
#EMAIL_HOST_USER = 'mdsimeone234@outlook.com'
#EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'eventhorizonjp@gmail.com'
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'app_name',
]

AUTH_USER_MODEL = 'app_name.User'

AUTHENTICATION_BACKENDS = [
	#'django.contrib.auth.backends.ModelBackend',
	'app_name.backends.UserBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
	'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'corsheaders.middleware.CorsPostCsrfMiddleware',
]

ROOT_URLCONF = 'project_name.urls'

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

WSGI_APPLICATION = 'project_name.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
} #if config('PYTHON_ENV', default='production') == 'development' else {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'd4bkbmcjedtp2g',
#        'USER': 'gevibcbynxcvpj',
#        'PASSWORD': 'b20f1778016d5a321ca60f78461ed7e139b99fef389961f93e66718eec157744',
#        'HOST': 'ec2-54-152-185-191.compute-1.amazonaws.com',
#        'PORT': '5432',
#    }
#}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/dist/'
STATIC_ROOT = os.path.join(BASE_DIR, 'dist')
#MEDIA_URL = 'media/'
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

FRONTEND_DIR = BASE_DIR

STATICFILES_DIRS = [
    os.path.join(FRONTEND_DIR, 'dist/static'),
]

# Webpack output location containing Vue index.html file
TEMPLATES[0]['DIRS'] += [
    os.path.join(FRONTEND_DIR, 'dist'),
]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Activate Django-Heroku.
django_heroku.settings(locals())
