"""
Django settings for NewsPaper project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-yfzrw7x^)33qy2t&jd#!ei#g7(+2l5abd_-z9vz%l(1&ux@@d%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # В боевом режиме поставить на False, чтобы не видеть отладочную инфу при ошибках

ALLOWED_HOSTS = ['127.0.0.1']  # Тут наш сайт: www:something.ru или IP адрес, пока ХЗ.


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # для создания аккаунта
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.yandex',  # http://127.0.0.1:8000/accounts/yandex/login/callback/

    'django.contrib.sites',  # Для простых страничек
    'django.contrib.flatpages',  # Для простых страничек

    'django_filters',  # django фильтры, из добавленной библиотеки ‘django_filters’

    'news.apps.NewsConfig',
    'accounts',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'NewsPaper.urls'

AUTHENTICATION_BACKENDS = [
    # Нужно войти по имени пользователя в Django admin, независимо от `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` специфические методы аутентификации, такие как логин по электронной почте
    'allauth.account.auth_backends.AuthenticationBackend',
]

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
            ],
        },
    },
]

LOGIN_URL = '/account/login/'
# LOGIN_REDIRECT_URL = "/account/profile/"  # Установить ссылку перехода после входа в систему
# LOGIN_REDIRECT_URL = "https://oauth.yandex.ru/verification_code"
# LOGIN_REDIRECT_URL = "/"
LOGIN_REDIRECT_URL = "login_redirect_url"
# ACCOUNT_LOGOUT_REDIRECT_URL = "/"  # Установить ссылку перехода после выхода из системы

# Настройки для верификации
ACCOUNT_EMAIL_REQUIRED = True  # email является обязательным
ACCOUNT_UNIQUE_EMAIL = True  # email является уникальным
ACCOUNT_USERNAME_REQUIRED = False  # username теперь необязательный.
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # аутентификация будет происходить посредством электронной почты
ACCOUNT_EMAIL_VERIFICATION = 'none'  # верификация почты отсутствует

# Чтобы allauth распознал нашу форму как ту, что должна выполняться вместо формы по умолчанию
# нужно чтобы зарегистрированный пользователь сразу добавлялся в нужную группу
ACCOUNT_FORMS = {'signup': 'accounts.forms.BasicSignupForm'}

WSGI_APPLICATION = 'NewsPaper.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Если вы попытаетесь получить доступ к базе данных, которую вы не определили в своих DATABASES настройках,
# Django вызовет django.utils.connection.ConnectionDoesNotExist исключение
# ./manage.py migrate --database=users
DATABASES = {
    'users': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db.newspaper',
        'USER': 'SergNews',
        'PASSWORD': 'qwer',
        'HOST': 'localhost',
        'PORT': '5433'
    },
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
     }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru'  # 'en-us' Теперь на русском языке

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False  # True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'  # название папки в пути для статических файлов, префикс URL-адреса
STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # путь к общей папке static, используемой реальным веб-сервером
STATICFILES_DIRS = []  # [BASE_DIR / 'static']  # список путей для нестандартных папок static

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




