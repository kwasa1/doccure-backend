
import json
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


with open(BASE_DIR / "conf" / "secret.json", "r") as file:
    file = json.loads(file.read())



def get_secret(setting):
    try:
        return file[setting]
    except:
        raise ImproperlyConfigured


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.sites",
    # third party apps
    
    # third party services
    "algoliasearch_django",
    
    
    # internal apps
    "core",
    "account",
    "facility",
    "disabledAccount",
    "authentication",
    "chats",
    
    
    # for disabled account
    
    
    
    # for chats with patients and doctors
    
    
]
ALGOLIA = {
    "APPLICATION_ID": get_secret("ALGOLIA_APPLICATION_ID"),
    "API_KEY": get_secret("ALGOLIA_API_KEY"),
    "INDEX_PREFIX":"cfe"
}

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cfe.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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


# for chats and messages




DJANGO_MESSAGES_NOTIFY = False

WSGI_APPLICATION = 'cfe.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASE_ROUTERS  = ['conf.routers.ApplicationRouter']

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME":  get_secret("NAME"),
        "USER": get_secret("USER"),
        "PASSWORD":  get_secret("PASSWORD"),
        "HOST":  get_secret("HOST"),
        "PORT":  get_secret("PORT"),
    },
    
    'account': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': get_secret("ACC_NAME"),
       'USER': get_secret("ACC_USER"),
       'PASSWORD': get_secret("ACC_PASSWORD"),
       'HOST': get_secret("ACC_HOST"),
       'PORT': get_secret("ACC_PORT"),
   }
}


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

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = get_secret("EMAIL_HOST")
# EMAIL_HOST_USER = get_secret("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = get_secret("EMAIL_HOST_PASSWORD")
# EMAIL_PORT = get_secret("EMAIL_PORT")
# EMAIL_USE_SSL = get_secret("EMAIL_USE_SSL")



AUTH_USER_MODEL = 'account.CustomUser'


# LOGIN_REDIRECT_URL = "account:profile"
LOGOUT_REDIRECT_URL = "core:home_view"

LOGIN_URL = "account:login"
LOGOUT_URL = "account:logout"

REDIRECT_FIELD_NAME = 'next'



EMAIL_HOST = "smtp.sendgrid.net" 
EMAIL_PORT = 587 
EMAIL_USE_TLS = True 
EMAIL_HOST_USER = "apikey"
EMAIL_HOST_PASSWORD = get_secret("SENDGRID_API_KEY")

DEFAULT_FROM_EMAIL = get_secret("DEFAULT_FROM_EMAIL")
DEFAULT_FROM_NAME = get_secret("DEFAULT_FROM_NAME")


LOGIN_REDIRECT_URL = "core:home_view"

ACCOUNT_SID = get_secret("ACCOUNT_SID")
AUTH_TOKEN = get_secret("AUTH_TOKEN")
SERVICE_SID = get_secret("SERVICE_SID")
TEMPLATE_ID = get_secret("TEMPLATE_ID")



AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "authentication.auth_backend.PasswordLessAuthentication"
)