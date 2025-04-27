from core.ckeditor import BASE_CKEDITOR_5_CONFIGS
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()

ENV_FILE_PATH = BASE_DIR.parent / "development.env"

environ.Env.read_env(env_file=ENV_FILE_PATH)

SECRET_KEY = env('DJANGO_SECRET_KEY', default="dsadsaldadsaskdladkalsdkdald")

DEBUG = env.bool('DJANGO_DEBUG', default=True)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['*'])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    # Internal Apps
    'account.apps.AccountConfig',
    'campaign.apps.CampaignConfig',
    'checkout.apps.CheckoutConfig',
    'main.apps.MainConfig',
    'cms.apps.CmsConfig',
    'api.apps.ApiConfig',
    # External Apps
    'django_ckeditor_5',
    'mptt',
    'nested_admin',
    'rest_framework',
    'django_filters',
    'import_export',
    'drf_spectacular',
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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "templates/"
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.context_processors.Default',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DB_ENGINE = env("DB_ENGINE", default="sqlite3")
if DB_ENGINE == "postgresql":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('DB_NAME', default='mydatabase'),
            'USER': env('DB_USER', default='myuser'),
            'PASSWORD': env('DB_PASSWORD', default='mypassword'),
            'HOST': env('DB_HOST', default='localhost'),
            'PORT': env('DB_PORT', default='5432'),
        }
    }
elif DB_ENGINE == "mysql":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': env("DB_NAME", default='mydatabase'),
            'USER': env("DB_USER", default='myuser'),
            'PASSWORD': env("DB_PASSWORD", default='mypassword'),
            'HOST': env("DB_HOST", default='localhost'),
            'PORT': env("DB_PORT", default='5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "uploads/"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "account.User"

AUTHENTICATION_BACKENDS = [
    'account.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# REST Framework Settings
REST_FRAMEWORK = {
    # Authentication Settings
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',  # Rate limiting for anonymous users
        'rest_framework.throttling.UserRateThrottle',  # Rate limiting for authenticated users
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',  # Limit anonymous users to 100 requests per day
        'user': '1000/day',  # Limit authenticated users to 1000 requests per day
    },

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,

}

STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY", default="sk_***")
STRIPE_PUBLISHABLE_KEY = env("STRIPE_PUBLISHABLE_KEY", default="pk_***")
STRIPE_WEBHOOK_KEY = env("STRIPE_WEBHOOK_KEY", default="whsec_***")

BASE_DOMAIN = env("BASE_DOMAIN", default="http://127.0.0.1:8000")

if not DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
            'LOCATION': env('MEMCACHE_HOST', default='127.0.0.1:11211'),
        }
    }
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_PORT = env("EMAIL_PORT", default="")
EMAIL_USE_TLS = env("EMAIL_USE_TLS", default="")
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_password", default="")

RABBITMQ_HOST = env("RABBITMQ_HOST")
RABBITMQ_PORT = env("RABBITMQ_PORT")
RABBITMQ_USER = env("RABBITMQ_USER")
RABBITMQ_PASSWORD = env("RABBITMQ_PASSWORD")
RABBITMQ_QUEUE_NAME = env("RABBITMQ_QUEUE_NAME")
RABBITMQ_VHOST = env("RABBITMQ_VHOST")

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/1'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TASK_TIME_LIMIT = 300  # Task time limit in seconds
CELERY_TASK_RETRY = True
CELERY_TASK_DEFAULT_RETRY_DELAY = 60
CELERY_TASK_MAX_RETRIES = 3
CELERY_TIMEZONE = 'UTC'
CELERY_BEAT_SCHEDULE = {
    # Example: 'task_name': {'task': 'task_path', 'schedule': 'interval_or_cron'}
}

# Enable Celery logging (if you want to see detailed Celery logs)
CELERYD_HIJACK_ROOT_LOGGER = False

EXTERNAL_API_BASE_URL = env("EXTERNAL_API_BASE_URL", default="")

CALLBACK_API_ENDPOINT = env("CALLBACK_API_ENDPOINT", default="")

CKEDITOR_5_CONFIGS = BASE_CKEDITOR_5_CONFIGS

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'DEBUG',
    },
}

STATIC_VERSION = "1"


SPECTACULAR_SETTINGS = {
    'TITLE': 'Zoomreachout API',
    'DESCRIPTION': '',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}