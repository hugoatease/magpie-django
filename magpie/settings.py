# Django settings for magpie project.
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

# Localization settings
TIME_ZONE = config.get('intl', 'timezone')
LANGUAGE_CODE = config.get('intl', 'language')
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Authentication settings
LOGIN_URL = "/account/login"
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

# Static files settings
STATIC_ROOT = config.get('static', 'root')
STATIC_URL = config.get('static', 'url')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_assets.finders.AssetsFinder',
)
ASSETS_MODULES = ['magpie.assets']

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
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
    'bootstrap3',
    'django_assets',
    'magpie',
    'magpie.servers',
    'magpie.account',
    'magpie.management',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "magpie.context.siteconf",
    "magpie.context.is_on_vpn",
)

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