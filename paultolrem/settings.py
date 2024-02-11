import os
from pathlib import Path
from decouple import config

INSTANCE_CONNECTION_NAME = 'glass-stratum-383701:europe-west1:instanciaperronalav44z'


# Use a Unix socket to connect to the instance when running on App Engine
if os.getenv('GAE_APPLICATION', None):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'db_perrona_66z',
            'USER': 'postgres',
            'PASSWORD': '8^]]CL-jFFsVlPZD',
            'HOST': '/cloudsql/' + INSTANCE_CONNECTION_NAME,
            'PORT': '',
        }
    }
    

else:
    # Local database configuration
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'db_perrona_66z',
            'USER': 'postgres',
            'PASSWORD': 'espejo risa 12',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
'''
# Local database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_perrona_66z',
        'USER': 'postgres',
        'PASSWORD': '8^]]CL-jFFsVlPZD',
        'HOST': '/cloudsql/glass-stratum-383701:europe-west1:instanciaperronalav44z',
        'PORT': '5432',
    }
}
'''

STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = 'glass-stratum-383701.appspot.com'
GS_PROJECT_ID = 'glass-stratum-383701'
GS_QUERYSTRING_AUTH = False

# Para usar HTTPS al servir archivos estáticos en producción
GS_DEFAULT_ACL = 'publicRead'
GS_BUCKET_ACL = 'publicRead'
GS_FILE_OVERWRITE = False

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-)eau#hk&*dreo*%##&delrt=l(d&(oxnht4)ee$z3_ikzxte&t'

DEBUG = False ### production
# DEBUG = True ### no production

ALLOWED_HOSTS = ['paultolrem.com', 
                 'www.paultolrem.com', 
                 'glass-stratum-383701.ew.r.appspot.com'
                ]

AUTH_USER_MODEL = 'registration.User'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'registration',
    'pricing',
    'charts',
    'info',
    'phone_field',
    'django_countries',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '3600/day',
        'user': '3600/hour'
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

SECURE_SSL_REDIRECT = True
ROOT_URLCONF = 'paultolrem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Add this line
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

WSGI_APPLICATION = 'paultolrem.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'charts/static'),  # Add this line
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
