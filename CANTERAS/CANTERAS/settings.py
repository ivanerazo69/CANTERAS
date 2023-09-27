""" 
Django settings for CANTERAS project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
#-------------------------------------------//-------------------------------------------
from pathlib import Path
import os
import sys
import logging
#-------------------------------------------//-------------------------------------------
# Build paths inside the project like this: BASE_DIR / 'subdir'.
#esto permite que apunte al directorio raíz del proyecto.
BASE_DIR = Path(__file__).resolve().parent.parent

#-------------------------------------------//-------------------------------------------
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pcc(-ic$=jd=38yd33rzl##u9*yxx*+2#0f6+pml4poz1ft&i_'
#-------------------------------------------//-------------------------------------------
# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
DEBUG = True
ALLOWED_HOSTS = []

#-------------------------------------------//-------------------------------------------
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ProyectoWebApp',
    'Busqueda',
    'Dashboard',
    'Procesos',
    'Soluciones',
]
#------//-------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'CANTERAS.urls'
#------//-------
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

WSGI_APPLICATION = 'CANTERAS.wsgi.application'
#-------------------------------------------//-------------------------------------------

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'CANTERAS',
        'USER': 'postgres',
        'PASSWORD': 'futuro10',
        'HOST': 'localhost',
        'PORT':5432
    }
}
#-------------------------------------------//-------------------------------------------
# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

#-------------------------------------------//-------------------------------------------
# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'es-eu'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
#-------------------------------------------//-------------------------------------------

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
#creamos las variables con los siguientes directorios para que maneje archivos multimedia en localhost
MEDIA_URL='/media/' #url pública para nuestros archivos, está aparecerá en la barra del navegador
MEDIA_ROOT=os.path.join(BASE_DIR, 'media') #en este caso se busca la carpeta 'media'
#STATIC_ROOT=os.path.join(BASE_DIR, 'static')#en este caso se busca la carpeta 'static'
#-------------------------------------------//-------------------------------------------
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#problemas con el navegador para mostrar el grafo
X_FRAME_OPTIONS = 'SAMEORIGIN'
#-------------------------------------------//-------------------------------------------

# Configuración de los registros
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',  # Puedes ajustar el nivel de depuración según tus necesidades
    },
}