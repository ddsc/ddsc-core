import os

import django.conf.global_settings as DEFAULT_SETTINGS

from lizard_ui.settingshelper import setup_logging
from lizard_ui.settingshelper import STATICFILES_FINDERS

DEBUG = True
TEMPLATE_DEBUG = True
TIME_ZONE = 'UTC'
USE_TZ = True

# SETTINGS_DIR allows media paths and so to be relative to this settings file
# instead of hardcoded to c:\only\on\my\computer.
SETTINGS_DIR = os.path.dirname(os.path.realpath(__file__))

# BUILDOUT_DIR is for access to the "surrounding" buildout, for instance for
# BUILDOUT_DIR/var/static files to give django-staticfiles a proper place
# to place all collected static files.
BUILDOUT_DIR = os.path.abspath(os.path.join(SETTINGS_DIR, '..'))
LOGGING = setup_logging(BUILDOUT_DIR, sql=True)

# ENGINE: 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
# In case of geodatabase, prepend with:
# django.contrib.gis.db.backends.(postgis)
DATABASES = {
    # If you want to use another database, consider putting the database
    # settings in localsettings.py. Otherwise, if you change the settings in
    # the current file and commit them to the repository, other developers will
    # also use these settings whether they have that database or not.
    # One of those other developers is Jenkins, our continuous integration
    # solution. Jenkins can only run the tests of the current application when
    # the specified database exists. When the tests cannot run, Jenkins sees
    # that as an error.
    'default': {
        'NAME': os.path.join(BUILDOUT_DIR, 'var', 'sqlite', 'test.db'),
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',  # empty string for localhost.
        'PORT': '',  # empty string for default.
        }
    }

CASSANDRA = {
    'servers': [
        '10.100.235.201:9160',
        '10.100.235.202:9160',
        '10.100.235.203:9160',
        '10.100.235.204:9160'
    ],
    'keyspace': 'ddsc_unittests',
    'batch_size': 10000,
}

SITE_ID = 1
SECRET_KEY = 'This is not secret but that is ok.'
INSTALLED_APPS = [
    'staticfiles',
    'compressor',
    'south',
    'django_nose',
    'django_extensions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.gis',
    'django.contrib.sites',
    'lizard_security',  # before lizard_ui!
    'lizard_ui',  # after lizard_security!
    'ddsc_core',  # after lizard_security!
    'treebeard',
    ]
ROOT_URLCONF = 'ddsc_core.urls'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'lizard_security.middleware.SecurityMiddleware',
    'tls.TLSRequestMiddleware',
    )

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Used for django-staticfiles (and for media files
STATIC_URL = '/static_media/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BUILDOUT_DIR, 'var', 'static')
MEDIA_ROOT = os.path.join(BUILDOUT_DIR, 'var', 'media')
STATICFILES_FINDERS = STATICFILES_FINDERS

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',  # treebeard
)

try:
    # Import local settings that aren't stored in svn/git.
    from ddsc_core.local_testsettings import *  # NOQA
except ImportError:
    pass
