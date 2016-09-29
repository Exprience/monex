"""
Django settings for monex project.

Generated by 'django-admin startproject' using Django 1.8.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import local_settings
from django.core.urlresolvers import reverse_lazy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_local(attr_name, default_value=None):
    if hasattr(local_settings, attr_name):
        return getattr(local_settings, attr_name)
    return default_value


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fuc40=#y)a(ey1&l$0g8)hui_n%n0mtldscmd+o1_za6&*6)lm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_local('DEBUG', False)

#TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'app.chat',
    'app.config',
    'app.user',
    'app.manager',
    'app.web',
    'app.competition',
    'app.online_support',
    'app.platform',
    
    'redactor',
    'captcha',
    'bootstrap3_datetime',
    
)



MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',


    'app.config.middleware.AuthMiddleware',
    'app.config.middleware.FlashMiddleware',
)

ROOT_URLCONF = 'monex.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'app/user/templates'),
            os.path.join(BASE_DIR, 'app/config/templates'),
            os.path.join(BASE_DIR, 'app/manager/templates'),
            os.path.join(BASE_DIR, 'app/competition/templates'),
            os.path.join(BASE_DIR, 'app/web/templates'),
            os.path.join(BASE_DIR, 'app/chat/templates'),
            os.path.join(BASE_DIR, 'app/online_support/templates'),
            ],
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

WSGI_APPLICATION = 'monex.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'monex.sqlite'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'mn'

USE_TZ = True

TIME_ZONE = 'Asia/Ulaanbaatar'

USE_I18N = True

USE_L10N = True

LOGGING_PATH = os.path.join(BASE_DIR, '.store', 'logs')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'file_app': {
            'level':'DEBUG',
            'class':'logging.FileHandler',
            'formatter':'standard',
            'filename': os.path.join(LOGGING_PATH, 'app.log'),
        },
    },
    'loggers': get_local('LOGGERS', {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'app': {
            'handlers': ['file_app'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }),
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "..", "www", "static")
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATIC_DOMAIN_URL = get_local('STATIC_DOMAIN_URL', '%s') % '/static/'


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


REDACTOR_OPTIONS = {'lang': 'en'}
REDACTOR_UPLOAD = 'uploads/'


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'uuganaaaaaa@gmail.com'
EMAIL_HOST_PASSWORD = 'niyxjmgailkagzjr'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'




LOGIN_URL = reverse_lazy('user:login')


CAPTCHA_FONT_SIZE = 30
CAPTCHA_IMAGE_SIZE = (90, 36)
CAPTCHA_LETTER_ROTATION = 0
CAPTCHA_TEXT_FIELD_TEMPLATE = 'config/captcha/captcha_text_field.html'


WS_SERVER=get_local('WS_SERVER', '192.168.1.20')

STATIC_DOMAIN_URL = get_local('STATIC_DOMAIN_URL', '%s') % '/static/'