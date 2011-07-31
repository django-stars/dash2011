# Django settings for presence project.

import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "apps"))


DEBUG = False

ADMINS = (
    ('Anton Agafonov', 'anton.agafonov@djangostars.com',),
    ('Roman Osipenko', 'roman.osipenko@djangostars.com',),
    ('Dizhak Vasyl', 'vasyl.dizhak@djangostars.com',),
)

MANAGERS = ADMINS

TIME_ZONE = 'Europe/Kiev'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), "media")

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(os.path.dirname(__file__), "static_collected")

STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = os.path.join(os.path.dirname(__file__), "static"),

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 's@#f*!-1^!#-jtql7$we=h)s0bqw0x0@!6bb+0v@^sodb#5w-s'

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
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'presence.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
    os.path.join(os.path.dirname(__file__), "..", "assets"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.csrf",
    "django.core.context_processors.i18n",
    "django.core.context_processors.static",
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.flatpages',

    # foreign appps
    'django_extensions',
    'south',
    'fresh_media',
    'pagination',

    # our apps
    'activity',
    'people',
    'workflow',
    'activation',
    'shout',
    'vote',
    'event',
    'planning',
)

LOCAL_DEVELOPMENT = True

AUTH_PROFILE_MODULE = 'people.Profile'

AUTHENTICATION_BACKENDS = (
    "apps.people.emailauth.EmailBackend",
    "apps.activation.backends.UrlLoginBackend",
    "django.contrib.auth.backends.ModelBackend",
    )

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = "/"
LOGOUT_URL = "/logout/"

DEFAULT_FROM_EMAIL = "presence@djangostars.com"
SHOUT_CONVERT_URL = True

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'dash@djangostars.com'
EMAIL_HOST_PASSWORD = 'dashdash'
EMAIL_PORT = 587

try:
    from settings_local import *
except ImportError:
    pass

try:
    from local_settings import *
except ImportError:
    pass

TEMPLATE_DEBUG = DEBUG
