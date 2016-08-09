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
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'app.user',
    'app.manager',
    'app.web',
    #'app.chat',
    'app.competition',
    'app.online_support',
    
    'redactor',
    'bootstrap3_datetime',
    'pagination_bootstrap',
    'django_modalview',
    'simple_history',
    'captcha',
    'django.contrib.admindocs',
    'notifications',
    'app.chat.apps.ChatConfig'
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

    'pagination_bootstrap.middleware.PaginationMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'monex.get_username.RequestMiddleware',
)

ROOT_URLCONF = 'monex.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'app/user/Templates'),
            os.path.join(BASE_DIR, 'app/manager/Templates'),
            os.path.join(BASE_DIR, 'app/competition/Templates'),
            os.path.join(BASE_DIR, 'app/web/Templates'),
            os.path.join(BASE_DIR, 'app/chat/Templates'),
            os.path.join(BASE_DIR, 'app/online_support/Templates'),
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


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
	'default': {
       		'ENGINE': 'django.db.backends.mysql',
       		'NAME': 'monex',
       		'USER': 'monex',
       		'PASSWORD': 'monex_1',
       		'HOST': '127.0.0.1',
        	'PORT': '',
            }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'mn'

USE_TZ = True

TIME_ZONE = 'Asia/Ulaanbaatar'

USE_I18N = True

USE_L10N = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        # I always add this handler to facilitate separating loggings
        'log_file':{
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, '.store/logs/app.log'),
            'maxBytes': '16777216', # 16megabytes
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'apps': { # I keep all my of apps under 'apps' folder, but you can also add them one by one, and this depends on how your virtualenv/paths are set
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
    # you can also shortcut 'loggers' and just configure logging for EVERYTHING at once
    'root': {
        'handlers': ['console', 'mail_admins'],
        'level': 'INFO'
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'


STATIC_ROOT = os.path.join(BASE_DIR, "..", "www", "static")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    )

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



from django.core.urlresolvers import reverse_lazy

LOGIN_URL = reverse_lazy('user:login')


CAPTCHA_FONT_SIZE = 30
CAPTCHA_IMAGE_SIZE = (90, 36)
CAPTCHA_LETTER_ROTATION = 0
CAPTCHA_TEXT_FIELD_TEMPLATE = 'web/captcha/captcha_text_field.html'

AUTH_USER_EMAIL_UNIQUE = True