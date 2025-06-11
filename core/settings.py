import os
from pathlib import Path
from dotenv import load_dotenv
import logging
from django.utils import timezone

# Read .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') == 'True'

ALLOWED_HOSTS = []

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} [{process:d}] {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '''
                asctime: %(asctime)s
                levelname: %(levelname)s
                process: %(process)d
                module: %(module)s
                message: %(message)s
                pathname: %(pathname)s
                funcName: %(funcName)s
                lineno: %(lineno)d
            ''',
        },
    },
    'handlers': {
        # Development console handler
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        # Production console handler
        'production_console': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        # Application file handler
        'file_app': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'app.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        # Error file handler
        'file_errors': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'errors.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        # Admin email handler
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
            'formatter': 'verbose',
        },
        # JSON log handler (for log aggregation systems)
        'json_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'json.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'json',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        # Django framework logs
        'django': {
            'handlers': ['console', 'production_console', 'file_errors'],
            'level': 'INFO',
            'propagate': False,
        },
        # Database query logs
        'django.db.backends': {
            'handlers': ['file_app'] if DEBUG else [],  # Only log queries in debug
            'level': 'DEBUG',
            'propagate': False,
        },
        # Request errors
        'django.request': {
            'handlers': ['file_errors', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        # Security logs
        'django.security': {
            'handlers': ['file_errors', 'mail_admins'],
            'level': 'WARNING',
            'propagate': False,
        },
        # Your apps
        'accounts': {
            'handlers': ['console', 'file_app', 'json_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'home': {
            'handlers': ['console', 'file_app', 'json_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'vege': {
            'handlers': ['console', 'file_app', 'json_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console', 'file_app', 'json_file'],
        'level': 'DEBUG' if DEBUG else 'INFO',
    },
}


# Application definition

INSTALLED_APPS = [
    
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'widget_tweaks',
    'accounts',
    'home',
    'vege',
    'cart',
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
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'  #UTC

USE_I18N = True

USE_TZ = True 

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')

#STATICFILES_DIR = [os.path.join(BASE_DIR,'static')]
STATICFILES_DIRS = [BASE_DIR / 'static']



MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CONTACT_FORM_RECIPIENT = "goldy.g2001@gmail.com"



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'goldy.g2001@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


EMAIL_TIMEOUT = 10
EMAIL_USE_LOCALTIME = True


LOGIN_REDIRECT_URL = 'vege:recipes'  # Where to redirect after login
LOGOUT_REDIRECT_URL = 'accounts:login'  # Where to redirect after logout

PASSWORD_RESET_TIMEOUT = 14400  # 4 hours in seconds
#PASSWORD_RESET_TIMEOUT_DAYS = 1  # 1 day in days

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

JAZZMIN_SETTINGS = {
    "site_title": "Recipes",
    "show_ui_builder": True,
    
    "topmenu_links": [
        {"name": "Back to Recipes", "url": "Vege:recipes", "icon": "fas fa-home"},
        {"name": "Contact Us", "url": "home:contact_view", "icon": "fas fa-envelope"},
        {"name": "About Us", "url": "home:about", "icon": "fas fa-info-circle"},
        {"name": "Settings", "url": "accounts:account_management", "icon": "fas fa-cog"},
        
        {"app" : "accounts", "model": "user", "name": "Users", "icon": "fas fa-users", "permissions": ["auth.view_user"]},
        #{"app" : "vege", "new window": True}, {"app" : "home"}, {"app" : "accounts"},{"app" : "cart"},
        {"app" : "vege", "model": "recipe", "name": "Recipes", "icon": "fas fa-utensils", "permissions": ["vege.view_recipe"]}
    ],
    "custom_css": "path/to/custom.css",
    "custom_js": "path/to/custom.js",
    "show_sidebar": True,
    "show_sidebar_user": True,
    "show_sidebar_search": True,
    "show_sidebar_recent": True,
    "show_sidebar_favorites": True

}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-danger",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-danger",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "solar",
    "dark_mode_theme": "solar",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

