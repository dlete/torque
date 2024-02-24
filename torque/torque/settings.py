"""
Django settings for torque project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h$m%xv_@-fm@8+obbunx%%d%4y$4^#+61os@gkhi%q#bicsl5h'

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
# it generates a lot of "errors" in the console when debug is false. 
# The "errors" do not affect service though
DEBUG = False

# dlete, original
#ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apiv1.apps.Apiv1Config',
    'audits.apps.AuditsConfig',
    'catalogues.apps.CataloguesConfig',
    'core.apps.CoreConfig',
    'inventories.apps.InventoriesConfig',
    'rest_framework',
    'rest_framework_swagger',
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

ROOT_URLCONF = 'torque.urls'

TEMPLATES = [
    {   
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # dlete, this is the original
        #'DIRS': [],
        # dlete
        # so that we can have a base.html and set template inheritance
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'torque.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
'''
#dlete, begin. This is the original db.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
#dlete, end. This is the original db.
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'torque',
        'USER': 'torque',
        'PASSWORD': 'Friday13',
        'HOST': 'localhost',
        'PORT': '',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

# dlete, begin
# https://docs.djangoproject.com/en/1.7/intro/tutorial02/#customizing-your-project-s-templates
#STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, 'static'),
#        )
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core/static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
# dlete, end

# dlete, begin
# https://code.djangoproject.com/wiki/Fixtures
FIXTURE_DIRS = [
    #os.path.join(BASE_DIR, 'core/fixtures'),
]
# dlete, end

# dlete, begin
# https://simpleisbetterthancomplex.com/tutorial/2016/06/13/how-to-send-email.html
EMAIL_HOST = 'smtp.heanet.ie'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# username/password just for sending mail
EMAIL_HOST_USER = 'torque_app'
EMAIL_HOST_PASSWORD = 'Fai4ohai!ph4wah9'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# dlete, end

# dlete, begin, error reporting
# https://docs.djangoproject.com/en/1.11/howto/error-reporting/
ADMINS = [('Daniel Lete', 'daniel.lete@heanet.ie')]
SERVER_EMAIL = 'torque@presto.heanet.ie'
# dlete, end, error reporting

# dlete, begin
# https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-16-04
#STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
# dlete, end

# dlete, begin
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ],
}
# for swagger authentication
# http://marcgibbons.github.io/django-rest-swagger/settings/#authentication
# Django REST swagger
LOGIN_URL = 'rest_framework:login'
LOGOUT_URL = 'rest_framework:logout'

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    },
}
# dlete, end


# dlete, begin recomendations in "manage.py check --deploy"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
#SESSION_COOKIE_SECURE = True
#CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
# dlete, end
