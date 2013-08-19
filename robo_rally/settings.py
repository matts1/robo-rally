# Django settings for robo_rally project.
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

def absolute(*args):
    return [os.path.join(os.path.dirname(os.path.abspath(__file__)), a) for a in args]

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'roborallygame@gmail.com'
EMAIL_HOST_PASSWORD = 'AGuLAJ0rIjluL'

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'data.sqlite3',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Australia/Sydney'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = absolute(
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    'static'
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '_2$6fcl+q9c1%z2y^9=wuo7j-b6l_8@6*@3l3%ylnb9d6svpux'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'robo_rally.middleware.loginredirect.LoginRequiredMiddleware',
)

ROOT_URLCONF = 'robo_rally.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'robo_rally.wsgi.application'

TEMPLATE_DIRS = absolute('templates',)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin static:
    # 'django.contrib.admindocs',
    'robo_rally.courses',
    'robo_rally.auth',
    'robo_rally.game',
    'robo_rally.messages',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

AUTH_PROFILE_MODULE = 'auth.UserProfile'

HOME_URL = '/lobbies'
LOGIN_URL = '/'

NO_LOGIN_REQUIRED_URLS = set([
    'login',
    'register',
    'resetpwd',
    'doreset',
    'completereset',
])

ALWAYS_ALLOWED_URLS = set([
    'documentation',
    'instructions'
])

# ASYNC stuff
if DEBUG:
    ASYNC_BACKEND_URL = 'http://220.233.10.213:8001'
else:
    raise ValueError('Please define an asynchronous backend URL which everyone can connect on')

NONE = 0
NON_SELF = 1
ALL = 2
SELF = 3

VALID_ACTIONS = {
    'adduser': NON_SELF,
    'deleteuser': NON_SELF,
    'gotopickmap': ALL,
    'ping': NONE,
    'startgame': ALL,
    'dealhand': SELF,
    'move': ALL,
    'health': SELF,
    'swapcards': NONE,
    'playerready':NONE,
    'newobjective': SELF,
    'powerdown': NONE,
    'alert': ALL,
    'virtual': ALL,
    'restart': ALL,
    'options': SELF,
    'setoption': NONE,
}
