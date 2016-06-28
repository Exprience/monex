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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fuc40=#y)a(ey1&l$0g8)hui_n%n0mtldscmd+o1_za6&*6)lm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True#False
#TEMPLATE_DEBUG = DEBUG
#ALLOWED_HOSTS = ['*']


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
    'app.chat',
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
    'app.web.get_username.RequestMiddleware',
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
       		'HOST': 'localhost',
        	'PORT': '',
    }
}
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'


STATIC_ROOT = '/var/www/monex.com/static' #os.path.join(BASE_DIR, "..", "www", "static")

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

LOGIN_URL = reverse_lazy('login')


CAPTCHA_FONT_SIZE = 30
CAPTCHA_IMAGE_SIZE = (90, 36)
CAPTCHA_LETTER_ROTATION = 0
CAPTCHA_TEXT_FIELD_TEMPLATE = 'web/captcha/captcha_text_field.html'

AUTH_USER_EMAIL_UNIQUE = True