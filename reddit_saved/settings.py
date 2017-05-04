import os
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$thdq)9ao9yc7k55r%#-dp06y8g_zp&sl4(%0e!(#+mu&3#+c)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'reddit_saved',
    'storage',
    'reddit_accounts',

    'crispy_forms',
    'django_extensions',
    'rest_framework',
    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',
    'webpack_loader',
    'corsheaders',
    'haystack'

]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

CRISPY_TEMPLATE_PACK = 'bootstrap3'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

ROOT_URLCONF = 'reddit_saved.urls'
LOGIN_REDIRECT_URL = "/"
CORS_ORIGIN_ALLOW_ALL = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'reddit_saved', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'reddit_saved.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'reddit',
        'USER': 'swoop',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

AUTHENTICATION_BACKENDS = (
   'rest_framework_social_oauth2.backends.DjangoOAuth2',
   'social_core.backends.reddit.RedditOAuth2',
   'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_REDDIT_KEY = "SYpUYS_j-YgJOQ"
SOCIAL_AUTH_REDDIT_SECRET = "YY0Ch-i_gxFuSzcY4q5S-VTFT20"
SOCIAL_AUTH_REDDIT_AUTH_EXTRA_ARGUMENTS = {'duration': 'permanent'}

BROKER_URL = 'redis://localhost:6379/0'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'reddit_saved', 'static'),
)

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'static/',#os.path.join(BASE_DIR, 'reddit_saved', 'static/'), # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR, 'front/webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': ['.+\.hot-update.js', '.+\.map']
    }
}

if DEBUG:
    INTERNAL_IPS = ('127.0.0.1',)
    MIDDLEWARE_CLASSES += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    INSTALLED_APPS += (
        'debug_toolbar',
    )
    #     DEBUG_TOOLBAR_PANELS = [
    #         'debug_toolbar.panels.versions.VersionsPanel',
    #         'debug_toolbar.panels.timer.TimerPanel',
    #         'debug_toolbar.panels.settings.SettingsPanel',
    #         'debug_toolbar.panels.headers.HeadersPanel',
    #         'debug_toolbar.panels.request.RequestPanel',
    #         'debug_toolbar.panels.sql.SQLPanel',
    #         'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    #         'debug_toolbar.panels.templates.TemplatesPanel',
    #         'debug_toolbar.panels.cache.CachePanel',
    #         'debug_toolbar.panels.signals.SignalsPanel',
    #         'debug_toolbar.panels.logging.LoggingPanel',
    #         'debug_toolbar.panels.redirects.RedirectsPanel',
    #     ]
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }
