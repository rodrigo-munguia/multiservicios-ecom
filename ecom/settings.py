"""
Django settings for ecom project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
import json
import environ
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/


env = environ.Env()

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG now controlled by an environment variable which allows using the same file in dev and prod
DEBUG = env.bool('DEBUG', default=True)

# For dev environment
if DEBUG == True: 
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'django-insecure--ec-_fae+z^+bier#un8-k3zd^3fa(r1d%+&&kv++)bekb#jja'

    #ALLOWED_HOSTS = []
    # for railway --------------------------------------------
    #ALLOWED_HOSTS = ['*']  # for railway
    #STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
    #STATIC_ROOT =os.path.join(BASE_DIR, 'staticfiles')
    #------------------------------------------------------

    # Application definition
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',    
        'django.contrib.staticfiles',
        'django.contrib.sites',
        'whitenoise.runserver_nostatic',    
        'crispy_forms',
        "django_extensions",
        "sslserver",
        # allauth configuration----------------------------------
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        # ... include the providers you want to enable:     
        'allauth.socialaccount.providers.facebook',
        'allauth.socialaccount.providers.google',   
        #--------------------------------------------------------
        'django_apscheduler',      
        'core'
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'ecom.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR,"templates")],
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

    #WSGI_APPLICATION = 'ecom.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/4.1/ref/settings/#databases
    
    """
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    """
   

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
    TIME_ZONE = 'America/Mexico_City'
    USE_I18N = True
    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.1/howto/static-files/
    
     # for railway --------------------------------------------
    ALLOWED_HOSTS = ['*']  # for railway
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
    #STATIC_ROOT =os.path.join(BASE_DIR, 'staticfiles')
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    STATIC_URL = 'static/'

   # STATICFILES_DIRS = [
   #     os.path.join(BASE_DIR, 'static')
   # ]

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'images/')

    CRISPY_TEMPLATE_PACK = 'bootstrap4'

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    # Auth
    AUTHENTICATION_BACKENDS = [
        
        # Needed to login by username in Django admin, regardless of `allauth`
        'django.contrib.auth.backends.ModelBackend',

        # `allauth` specific authentication methods, such as login by e-mail
        'allauth.account.auth_backends.AuthenticationBackend',
        
    ]

    SOCIALACCOUNT_PROVIDERS = \
        {'facebook':
        {'METHOD': 'oauth2',
            'SCOPE': ['email','public_profile'],
            'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
            'FIELDS': [
                'id',
                'email',
                'name',
                'first_name',
                'last_name',
                'picture'],
            'EXCHANGE_TOKEN': True,
            'LOCALE_FUNC': lambda request: 'kr_KR',
            'VERIFIED_EMAIL': False,
            'VERSION': 'v2.4'},
        
        "google": {
            "SCOPE":[
                "profile",
                "email"
            ],
            "AUTH_PARAMS":{"a100ccess_type":"online"}
        }
        }
        
    # set the time (minutes) that an order can be active in the kart
    MINUTES_IN_KART = 1
    # set the time (hours) for sending a remainder to clients with not-completed pick-up orders
    HOURS_TO_REMAINDER_FOR_PICKUP_ORDERS = 12
    # set the time (hours) for cancel/delete pick-up orders that have not been complete
    HOURS_TO_CANCEL_PICKUP_ORDERS = 24    
        
    THUMB_SIZE = (200,200) # thumbail size in pixels

    SITE_ID = 2
    LOGIN_REDIRECT_URL = '/'
    LOGOUT_REDIRECT_URL = '/'

    ACCOUNT_EMAIL_VERIFICATION = 'none' 
    
    # load personal config data
    f = open('personal_config.json')
    config = json.load(f)
    email = config['email'][0]
    stripe = config['stripe'][0]
    
    db = config['db'][0]
    
    
    # local database
    """
    DATABASES = {     
        'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': db['NAME'],
        'USER': db['USER'],
        'PASSWORD': db['PASSWORD'],
        'HOST': db['HOST'],
        'PORT': db['PORT']  
        } 
    } 
    """
    
    
    # remote database (railway app)
    
    railway_db = config['railway_db'][0]    
    DATABASE_URL = railway_db['DATABASE_URL']    
    DATABASES = {
    "default": dj_database_url.config(default=DATABASE_URL, conn_max_age=1800),
    }
    
                    
    STRIPE_SECRET_KEY = stripe["STRIPE_SECRET_KEY"]
    STRIPE_PUBLIC_KEY = stripe["STRIPE_PUBLIC_KEY"]
    STRIPE_WEBHOOK_KEY = stripe["STRIPE_WEBHOOK_KEY"]                 

    # -----email configuration ------------------------------------------------------
    # for configuring gmail: https://www.youtube.com/watch?v=iGPPhzhXBFg
    EMAIL_BACKEND = email["EMAIL_BACKEND"]
    EMAIL_HOST = email["EMAIL_HOST"]
    EMAIL_HOST_USER = email["EMAIL_HOST_USER"]
    EMAIL_HOST_PASSWORD = email["EMAIL_HOST_PASSWORD"] # app password (not regular password)
    EMAIL_PORT = email["EMAIL_PORT"]
    EMAIL_USE_TLS = email["EMAIL_USE_TLS"]
    #EMAIL_USE_SSL = email["EMAIL_USE_SSL"]
    # -------------------------------------------------------------------------------
else:
    # production environment
    DEBUG = True
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'django-insecure--ec-_fae+z^+bier#un8-k3zd^3fa(r1d%+&&kv++)bekb#jja'

    #ALLOWED_HOSTS = []
   

    # Application definition
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',    
        'django.contrib.staticfiles',
        'django.contrib.sites',            
        'crispy_forms',
        "django_extensions",
        "sslserver",
        # allauth configuration----------------------------------
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        # ... include the providers you want to enable:     
        'allauth.socialaccount.providers.facebook',
        'allauth.socialaccount.providers.google',   
        #--------------------------------------------------------
        'django_apscheduler',      
        'core'       
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',        
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware'        
    ]
    #'whitenoise.middleware.WhiteNoiseMiddleware',

    ROOT_URLCONF = 'ecom.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR,"templates")],
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

    WSGI_APPLICATION = 'ecom.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/4.1/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
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
    TIME_ZONE = 'America/Mexico_City'
    USE_I18N = True
    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.1/howto/static-files/
    
     # for railway --------------------------------------------
    ALLOWED_HOSTS = ['*']  # for railway
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
    #STATIC_ROOT =os.path.join(BASE_DIR, 'staticfiles')
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    #------------------------------------------------------
    
    STATIC_URL = 'static/'
    
   
    
    #STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    

    

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'images/')

    CRISPY_TEMPLATE_PACK = 'bootstrap4'

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    # Auth
    AUTHENTICATION_BACKENDS = [
        
        # Needed to login by username in Django admin, regardless of `allauth`
        'django.contrib.auth.backends.ModelBackend',

        # `allauth` specific authentication methods, such as login by e-mail
        'allauth.account.auth_backends.AuthenticationBackend',
        
    ]

    SOCIALACCOUNT_PROVIDERS = \
        {'facebook':
        {'METHOD': 'oauth2',
            'SCOPE': ['email','public_profile'],
            'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
            'FIELDS': [
                'id',
                'email',
                'name',
                'first_name',
                'last_name',
                'picture'],
            'EXCHANGE_TOKEN': True,
            'LOCALE_FUNC': lambda request: 'kr_KR',
            'VERIFIED_EMAIL': False,
            'VERSION': 'v2.4'},
        
        "google": {
            "SCOPE":[
                "profile",
                "email"
            ],
            "AUTH_PARAMS":{"access_type":"online"}
        }
        }
        
    # set the time (minutes) that an order can be active in the kart
    MINUTES_IN_KART = 1
    # set the time (hours) for sending a remainder to clients with not-completed pick-up orders
    HOURS_TO_REMAINDER_FOR_PICKUP_ORDERS = 12
    # set the time (hours) for cancel/delete pick-up orders that have not been complete
    HOURS_TO_CANCEL_PICKUP_ORDERS = 24    
        
    THUMB_SIZE = (200,200) # thumbail size in pixels

    SITE_ID = 2
    LOGIN_REDIRECT_URL = '/'
    LOGOUT_REDIRECT_URL = '/'

    ACCOUNT_EMAIL_VERIFICATION = 'none' 
    
    # production environment
    CSRF_TRUSTED_ORIGINS = ['https://*.up.railway.app/']
       
    
    DATABASE_URL = env('DATABASE_URL', default='')
    
    DATABASES = {
    "default": dj_database_url.config(default=DATABASE_URL, conn_max_age=1800),
    }
     
    
    STRIPE_SECRET_KEY   = env('STRIPE_SECRET_KEY', default='')
    STRIPE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY', default='')
    STRIPE_WEBHOOK_KEY = env('STRIPE_WEBHOOK_KEY', default='')
    
    EMAIL_BACKEND = env('EMAIL_BACKEND', default='')
    EMAIL_HOST = env('EMAIL_HOST', default='')
    EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
    EMAIL_PORT = env('EMAIL_PORT', default='')
    EMAIL_USE_TLS = env('EMAIL_USE_TLS', default='') 
    










# https://stripe.com/docs/webhooks/quickstart
# for testing stripe webhook: stripe listen --forward-to 127.0.0.1:9000/webhooks/stripe/   

# for testing https conections: https://github.com/teddziuba/django-sslserver
# python manage.py runsslserver
# in browser : https://localhost:8000  

# configure google auth guide: https://www.youtube.com/watch?v=yO6PP0vEOMc
# configure facebook auth: https://www.codesnail.com/facebook-authentication-in-django-using-django-allauth/






