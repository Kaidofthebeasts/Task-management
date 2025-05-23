# CLoud project/task_manager_project/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv # Import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(os.path.join(BASE_DIR, '.env')) # <--- Add this line after BASE_DIR


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default-insecure-key-for-dev-only') # <-- Read from environment


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True' # <-- Read from environment

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',') # <-- Read from environment


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize', # For template filters like naturaltime
    'django_cleanup.apps.CleanupConfig', # For cleaning old files

    # Local apps
    'accounts',
    'tasks',
    'django_extensions', # For running scripts
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'task_manager_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'task_manager_project.context_processors.unread_notifications',
            ],
        },
    },
]

WSGI_APPLICATION = 'task_manager_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Reverted to SQLite3
        'NAME': BASE_DIR / 'db.sqlite3', # Reverted to SQLite3 database file
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/topics/i18n/password-validation/

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Addis_Ababa' # Set timezone to Addis Ababa

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles' # For collectstatic

# Media files (User uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.CustomUser'

# Redirect URLs
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

# Email Configuration for Password Reset and Notifications
# For development, you might use a console backend first:
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend') # <-- Read from environment

# For sending real emails (e.g., via Gmail SMTP):
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com') # <-- Read from environment
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587)) # <-- Read from environment (cast to int)
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True' # <-- Read from environment (cast to bool)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '') # <-- Read from environment
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '') # <-- Read from environment

# Default email address to use for various automated emails
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'webmaster@localhost') # <-- Read from environment
SERVER_EMAIL = os.getenv('SERVER_EMAIL', 'webmaster@localhost') # <-- Read from environment

# Base URL for email links (if you included it in signals.py)
BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1:8000')
