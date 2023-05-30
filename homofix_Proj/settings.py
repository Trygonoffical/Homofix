
from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-emn+k5ze0*u)aj-8%2yd9j!881g%q=)y_8@2f&p=93ktlesvo+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Application definition

INSTALLED_APPS = [
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'rest_framework',
    'rest_framework_simplejwt',
    "corsheaders",
    'homofix_app',
    
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
     "corsheaders.middleware.CorsMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'homofix_app.LoginCheckMiddleWare.LoginCheckMiddleWare'
]

ROOT_URLCONF = 'homofix_Proj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'homofix_Proj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'homofix',
        'USER': 'root',
       
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'homofix',
#         'HOST': 'database.caxj1wczqvkk.us-east-2.rds.amazonaws.com',
#         'USER': 'admin',
#         'PASSWORD': 'homofixcmp',   
#         'PORT': '3306',
#     }
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'homofix',
#         'USER': 'root',
       
#     }
# }


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

TIME_ZONE = 'Asia/Calcutta'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
STATIC_URL = '/static/'
STATIC_ROOT=os.path.join(BASE_DIR,'staticfiles')

# STATIC_URL = 'static/'
# STATIC_ROOT = os.path.join(BASE_DIR,'static/')




STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static/invoice')
    
   
    
]

MEDIA_ROOT =os.path.join(BASE_DIR,'media/Invoice')
MEDIA_URL='/media/'
# MEDIA_URL="/media/"
# MEDIA_ROOT=os.path.join(BASE_DIR,"media")


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL="homofix_app.CustomUser"

DATE_INPUT_FORMATS = [
    '%d-%m-%Y',
    '%Y-%m-%d',
    '%m/%d/%Y',
    # Add more formats here if needed
]


GOOGLE_MAPS_API_KEY = 'https://armaan.pythonanywhere.com/api/ExpertAllLocation/'

REST_FRAMEWORK = {
    
    'DEFAULT_AUTHENTICATION_CLASSES': (
        
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
    
}

# STATICFILES_DIRS = [
#     BASE_DIR / "homofixapp/static",
    
# ]




# settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtpout.secureserver.net'
EMAIL_HOST_USER = 'info@homofixcompany.com'
EMAIL_HOST_PASSWORD = 'Homofixcompany@139'
EMAIL_PORT = 465
EMAIL_USE_SSL = True

PASSWORD_RESET_URL = 'password_reset/'
DEFAULT_FROM_EMAIL = 'info@homofixcompany.com'




CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    # 'http://192.168.0.100:3000/',
    # 'https://support.homofixcompany.com/api/Verify/otp/'
] 