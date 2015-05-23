# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from ConfigParser import ConfigParser
config = ConfigParser()
config.read('magpie.ini')

# Django main settings
ALLOWED_HOSTS = ['*']
SECRET_KEY = config.get('magpie', 'secret')
WSGI_APPLICATION = 'magpie.wsgi.application'
ROOT_URLCONF = 'magpie.urls'

DEBUG = config.get('magpie', 'debug') == 'true'
TEMPLATE_DEBUG = DEBUG

# Magpie settings
BRAND_NAME = config.get('magpie', 'brand')
SERVER_EMAIL = config.get('magpie', 'server_email')
SELF_REGISTER = config.get('magpie', 'self_register') == 'true'

# Localization settings
TIME_ZONE = config.get('intl', 'timezone')
LANGUAGE_CODE = config.get('intl', 'language')
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = (BASE_DIR + '/translations',)

# Authentication settings
LOGIN_URL = "/account/login/"
LOGIN_REDIRECT_URL = "/"

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.' + config.get('database', 'engine'),
        'NAME': config.get('database', 'name'),
    }
}
if config.has_option('database', 'user'):
    DATABASES['default']['USER'] = config.get('database', 'user')
if config.has_option('database', 'password'):
    DATABASES['default']['PASSWORD'] = config.get('database', 'password')
if config.has_option('database', 'host'):
    DATABASES['default']['HOST'] = config.get('database', 'host')
if config.has_option('database', 'port'):
    DATABASES['default']['PORT'] = config.get('database', 'port')

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'rest_framework',
    'oauth2_provider',
    'djangobower',
    'pipeline',
    'bootstrap3',
    'magpie',
    'magpie.servers',
    'magpie.account',
    'magpie.management',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.template.context_processors.request",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "magpie.context.siteconf",
    "magpie.context.is_on_vpn",
)

# Static files settings
STATIC_ROOT = config.get('static', 'root')
STATIC_URL = config.get('static', 'url')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
    'pipeline.finders.PipelineFinder',
)

BOWER_COMPONENTS_ROOT = BASE_DIR
BOWER_INSTALLED_APPS = (
    'bootstrap#3.0.0',
    'font-awesome#3.2.1',
)

PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.NoopCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.NoopCompressor'

PIPELINE_CSS = {
    'magpie': {
        'source_filenames': (
            'bootstrap/dist/css/bootstrap.min.css',
            'font-awesome/css/font-awesome.min.css',
        ),
        'output_filename': 'assets/magpie.css'
    }
}

PIPELINE_JS = {
    'magpie': {
        'source_filenames': (
            'jquery/dist/jquery.min.js',
            'bootstrap/dist/js/bootstrap.min.js',
        ),
        'output_filename': 'assets/magpie.js'
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'magpie.api.permissions.IsAdminOrAuthenticatedRead',
    )
}

OAUTH2_PROVIDER = {
    'OAUTH2_VALIDATOR_CLASS': 'magpie.api.oauth2.ApiOAuth2Validator',
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
        'service': 'OpenVPN nodes access'
    }
}

OAUTH2_PROVIDER_APPLICATION_MODEL = 'magpie.VPNApplication'