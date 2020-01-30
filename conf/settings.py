"""
Django settings for ui project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

import environ

from directory_constants import cms
import directory_healthcheck.backends
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


env = environ.Env()
for env_file in env.list('ENV_FILES', default=[]):
    env.read_env(f'conf/env/{env_file}')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', False)

# As the app is running behind a host-based router supplied by Heroku or other
# PaaS, we can open ALLOWED_HOSTS
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.forms',
    'core',
    'directory_constants',
    'captcha',
    'sorl.thumbnail',
    'directory_components',
    'health_check.cache',
    'directory_healthcheck',
    'euexit',
    'perfect_fit_prospectus',
    'invest',
    'investment_support_directory',
    'find_a_supplier',
    'contact',
]

MIDDLEWARE = [
    'directory_components.middleware.MaintenanceModeMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'directory_components.middleware.LocaleQuerystringMiddleware',
    'directory_components.middleware.ForceDefaultLocale',
    'directory_components.middleware.PersistLocaleMiddleware',
    'directory_components.middleware.CountryMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'core.middleware.GoogleCampaignMiddleware',
    'directory_components.middleware.NoCacheMiddlware',
    'directory_components.middleware.CheckGATags'
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.footer_contact_us_link',
                'core.context_processors.services_home_links',
                'core.context_processors.header_navigation',
                'directory_components.context_processors.analytics',
                'directory_components.context_processors.urls_processor',
                'directory_components.context_processors.cookie_notice',
                'directory_components.context_processors.feature_flags',
                'directory_components.context_processors.header_footer_processor',
                'core.context_processors.directory_components_html_lang_attribute',
            ],
        },
    },
]

WSGI_APPLICATION = 'conf.wsgi.application'

VCAP_SERVICES = env.json('VCAP_SERVICES', {})

if 'redis' in VCAP_SERVICES:
    REDIS_URL = VCAP_SERVICES['redis'][0]['credentials']['uri']
else:
    REDIS_URL = env.str('REDIS_URL', '')

if REDIS_URL:
    cache = {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': "django_redis.client.DefaultClient",
        }
    }
else:
    cache = {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }


CACHES = {
    'default': cache,
    'cms_fallback': cache,
    'api_fallback': cache
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGE_COOKIE_NAME = env.str('LANGUAGE_COOKIE_NAME', 'django_language')
# https://docs.djangoproject.com/en/2.2/ref/settings/#std:setting-LANGUAGE_COOKIE_NAME
LANGUAGE_COOKIE_DEPRECATED_NAME = 'django-language'

# Django's default value for LANGUAGE_COOKIE_DOMAIN is None
LANGUAGE_COOKIE_DOMAIN = env.str('LANGUAGE_COOKIE_DOMAIN', None)

# https://github.com/django/django/blob/master/django/conf/locale/__init__.py
LANGUAGES = [
    ('en-gb', 'English'),               # English
    ('de', 'Deutsch'),                  # German
    ('ja', '日本語'),                    # Japanese
    ('zh-hans', '简体中文'),             # Simplified Chinese
    ('fr', 'Français'),                 # French
    ('es', 'español'),                  # Spanish
    ('pt', 'Português'),                # Portuguese
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

FEATURE_MAINTENANCE_MODE_ENABLED = env.bool(
    'FEATURE_MAINTENANCE_MODE_ENABLED', False
)

# Invest High Potential Opportunities
HPO_GOV_NOTIFY_AGENT_EMAIL_ADDRESS = env.str('HPO_GOV_NOTIFY_AGENT_EMAIL_ADDRESS',)
HPO_GOV_NOTIFY_AGENT_TEMPLATE_ID = env.str('HPO_GOV_NOTIFY_AGENT_TEMPLATE_ID', '064e2801-18f4-4342-a9e3-5eecddfa7d04')
HPO_GOV_NOTIFY_USER_TEMPLATE_ID = env.str('HPO_GOV_NOTIFY_USER_TEMPLATE_ID', 'a9285cb0-6acf-428f-94f7-2da7248d9ef0')
HPO_GOV_NOTIFY_USER_REPLY_TO_ID = env.str('HPO_GOV_NOTIFY_USER_REPLY_TO_ID', '3deb5fc2-1032-4352-aa0a-c677548a9f02')

# Brexit
EU_EXIT_ZENDESK_SUBDOMAIN = env.str('EU_EXIT_ZENDESK_SUBDOMAIN')
EU_EXIT_INTERNATIONAL_CONTACT_URL = env.str(
    'EU_EXIT_INTERNATIONAL_CONTACT_URL', '/international/eu-exit-news/contact/'
)

# Contact
INVEST_CONTACT_URL = env.str('INVEST_CONTACT_URL', 'https://invest.great.gov.uk/contact/')
FIND_A_SUPPLIER_CONTACT_URL = env.str('FIND_A_SUPPLIER_CONTACT_URL', 'https://trade.great.gov.uk/industries/contact/')
CONTACT_INTERNATIONAL_ZENDESK_SUBJECT = env.str(
    'CONTACT_DOMESTIC_ZENDESK_SUBJECT', 'great.gov.uk international contact form'
)

# needed only for dev local storage
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

# Static files served with Whitenoise and AWS Cloudfront
# http://whitenoise.evans.io/en/stable/django.html#instructions-for-amazon-cloudfront
# http://whitenoise.evans.io/en/stable/django.html#restricting-cloudfront-to-static-files
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_HOST = env.str('STATIC_HOST', '')
STATIC_URL = STATIC_HOST + '/static/'
STATICFILES_STORAGE = env.str(
    'STATICFILES_STORAGE',
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
)

# Logging for development
if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': True,
            },
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
        }
    }

# Sentry
if env.str('SENTRY_DSN', ''):
    sentry_sdk.init(
        dsn=env.str('SENTRY_DSN'),
        environment=env.str('SENTRY_ENVIRONMENT'),
        integrations=[DjangoIntegration()]
    )


ANALYTICS_ID = env.str('ANALYTICS_ID', '')

SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', True)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', 16070400)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
LANGUAGE_COOKIE_SECURE = env.bool('LANGUAGE_COOKIE_SECURE', True)
COUNTRY_COOKIE_SECURE = env.bool('COUNTRY_COOKIE_SECURE', True)

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', True)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_NAME = env.str('SESSION_COOKIE_NAME', 'great_int_sessionid')
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', True)
CSRF_COOKIE_HTTPONLY = True

# Google Recaptcha
RECAPTCHA_PUBLIC_KEY = env.str('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = env.str('RECAPTCHA_PRIVATE_KEY')
# NOCAPTCHA = True turns on version 2 of recaptcha
NOCAPTCHA = env.bool('NOCAPTCHA', True)

# Google tag manager
GOOGLE_TAG_MANAGER_ID = env.str('GOOGLE_TAG_MANAGER_ID', '')
GOOGLE_TAG_MANAGER_ENV = env.str('GOOGLE_TAG_MANAGER_ENV', '')
UTM_COOKIE_DOMAIN = env.str('UTM_COOKIE_DOMAIN')
PRIVACY_COOKIE_DOMAIN = env.str('PRIVACY_COOKIE_DOMAIN', '')

# django-storages for thumbnails
AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY', '')
AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID', '')
AWS_STORAGE_BUCKET_NAME = env.str('AWS_STORAGE_BUCKET_NAME', '')
AWS_DEFAULT_ACL = None
AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_ENCRYPTION = True
AWS_S3_FILE_OVERWRITE = False
AWS_S3_CUSTOM_DOMAIN = env.str('AWS_S3_CUSTOM_DOMAIN', '')
AWS_S3_REGION_NAME = env.str('AWS_S3_REGION_NAME', 'eu-west-1')
AWS_S3_URL_PROTOCOL = env.str('AWS_S3_URL_PROTOCOL', 'https:')
# Needed for new AWS regions
# https://github.com/jschneier/django-storages/issues/203
AWS_S3_SIGNATURE_VERSION = env.str('AWS_S3_SIGNATURE_VERSION', 's3v4')
AWS_QUERYSTRING_AUTH = env.bool('AWS_QUERYSTRING_AUTH', False)
S3_USE_SIGV4 = env.bool('S3_USE_SIGV4', True)
AWS_S3_HOST = env.str('AWS_S3_HOST', 's3.eu-west-1.amazonaws.com')

PREFIX_DEFAULT_LANGUAGE = False

# directory CMS
DIRECTORY_CMS_API_CLIENT_BASE_URL = env.str('CMS_URL')
DIRECTORY_CMS_API_CLIENT_API_KEY = env.str('CMS_SIGNATURE_SECRET')
DIRECTORY_CMS_API_CLIENT_SENDER_ID = 'directory'
DIRECTORY_CMS_API_CLIENT_SERVICE_NAME = cms.GREAT_INTERNATIONAL
DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT = env.int('DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT', 2)
DIRECTORY_CMS_SITE_ID = env.str('DIRECTORY_CMS_SITE_ID', 2)

# directory clients
DIRECTORY_CLIENT_CORE_CACHE_EXPIRE_SECONDS = env.int(
    'DIRECTORY_CLIENT_CORE_CACHE_EXPIRE_SECONDS',
    60 * 60 * 24 * 30  # 30 days
)

# directory API client
DIRECTORY_API_CLIENT_BASE_URL = env.str('DIRECTORY_API_CLIENT_BASE_URL')
DIRECTORY_API_CLIENT_API_KEY = env.str('DIRECTORY_API_CLIENT_API_KEY')
DIRECTORY_API_CLIENT_SENDER_ID = env.str('DIRECTORY_API_CLIENT_SENDER_ID', 'directory')
DIRECTORY_API_CLIENT_DEFAULT_TIMEOUT = env.int('DIRECTORY_API_CLIENT_DEFAULT_TIMEOUT', 15)

# directory forms api client
DIRECTORY_FORMS_API_BASE_URL = env.str('DIRECTORY_FORMS_API_BASE_URL')
DIRECTORY_FORMS_API_API_KEY = env.str('DIRECTORY_FORMS_API_API_KEY')
DIRECTORY_FORMS_API_SENDER_ID = env.str('DIRECTORY_FORMS_API_SENDER_ID')
DIRECTORY_FORMS_API_DEFAULT_TIMEOUT = env.int('DIRECTORY_API_FORMS_DEFAULT_TIMEOUT', 5)
DIRECTORY_FORMS_API_ZENDESK_SEVICE_NAME = env.str('DIRECTORY_FORMS_API_ZENDESK_SEVICE_NAME', 'directory')

CONTACT_ISD_COMPANY_NOTIFY_TEMPLATE_ID = env.str(
    'CONTACT_ISD_COMPANY_NOTIFY_TEMPLATE_ID', 'a0ffc316-09f0-4b28-9af0-86243645efca'
)
CONTACT_ISD_SUPPORT_NOTIFY_TEMPLATE_ID = env.str(
    'CONTACT_ISD_SUPPORT_NOTIFY_TEMPLATE_ID', '19fc13d1-fcc1-4e3b-a488-244a520742e2'
)
CONTACT_ISD_INVESTOR_NOTIFY_TEMPLATE_ID = env.str(
    'CONTACT_ISD_INVESTOR_NOTIFY_TEMPLATE_ID', '351e32e9-2e66-4a6f-8b20-a9942f045f1b'
)
CONTACT_ISD_SUPPORT_EMAIL_ADDRESS = env.str('CONTACT_ISD_SUPPORT_EMAIL_ADDRESS', '')
CONTACT_FAS_COMPANY_NOTIFY_TEMPLATE_ID = env.str(
    'CONTACT_FAS_COMPANY_NOTIFY_TEMPLATE_ID', 'bb88aa79-595a-44fc-9ed3-cf8a6cbd6306'
)

# Contact email
DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL')
IIGB_AGENT_EMAIL = env.str('IIGB_AGENT_EMAIL')
CAPITAL_INVEST_CONTACT_EMAIL = env.str('CAPITAL_INVEST_CONTACT_EMAIL')
EMAIL_BACKED_CLASSES = {
    'default': 'django.core.mail.backends.smtp.EmailBackend',
    'console': 'django.core.mail.backends.console.EmailBackend'
}
EMAIL_BACKEND_CLASS_NAME = env.str('EMAIL_BACKEND_CLASS_NAME', 'default')
EMAIL_BACKEND = EMAIL_BACKED_CLASSES[EMAIL_BACKEND_CLASS_NAME]
EMAIL_HOST = env.str('EMAIL_HOST', '')
EMAIL_PORT = env.int('EMAIL_HOST_PORT', 587)
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = True

# LINKS TO OTHER SERVICES
DIRECTORY_CONSTANTS_URL_GREAT_DOMESTIC = env.str('DIRECTORY_CONSTANTS_URL_GREAT_DOMESTIC', '')
DIRECTORY_CONSTANTS_URL_INTERNATIONAL = env.str('DIRECTORY_CONSTANTS_URL_INTERNATIONAL', '')
DIRECTORY_CONSTANTS_URL_EXPORT_OPPORTUNITIES = env.str('DIRECTORY_CONSTANTS_URL_EXPORT_OPPORTUNITIES', '')
DIRECTORY_CONSTANTS_URL_SELLING_ONLINE_OVERSEAS = env.str('DIRECTORY_CONSTANTS_URL_SELLING_ONLINE_OVERSEAS', '')
DIRECTORY_CONSTANTS_URL_EVENTS = env.str('DIRECTORY_CONSTANTS_URL_EVENTS', '')
DIRECTORY_CONSTANTS_URL_INVEST = env.str('DIRECTORY_CONSTANTS_URL_INVEST', '')
DIRECTORY_CONSTANTS_URL_FIND_A_SUPPLIER = env.str('DIRECTORY_CONSTANTS_URL_FIND_A_SUPPLIER', '')
DIRECTORY_CONSTANTS_URL_SINGLE_SIGN_ON = env.str('DIRECTORY_CONSTANTS_URL_SINGLE_SIGN_ON', '')
DIRECTORY_CONSTANTS_URL_FIND_A_BUYER = env.str('DIRECTORY_CONSTANTS_URL_FIND_A_BUYER', '')

# feature flags
FEATURE_FLAGS = {
    'HOW_TO_DO_BUSINESS_ON': env.bool('FEATURE_HOW_TO_DO_BUSINESS_ENABLED', False),
    'INTERNATIONAL_CONTACT_LINK_ON': env.bool('FEATURE_INTERNATIONAL_CONTACT_LINK_ENABLED', False),
    'MAINTENANCE_MODE_ON': env.bool('FEATURE_MAINTENANCE_MODE_ENABLED', False),
    'RECOMMENDED_FOR_CHOSEN_COUNTRY_ON': env.bool('FEATURE_RECOMMENDED_FOR_CHOSEN_COUNTRY_ENABLED', False),
    'COUNTRY_SELECTOR_ON': env.bool('FEATURE_COUNTRY_SELECTOR_ENABLED', False),
    'CAPITAL_INVEST_REGION_PAGE_ON': env.bool('FEATURE_CAPITAL_INVEST_REGION_PAGE_ENABLED', False),
    'ABOUT_UK_REGION_PAGE_ON': env.bool('FEATURE_ABOUT_UK_REGION_PAGE_ENABLED', False),
    'ABOUT_UK_REGION_LISTING_PAGE_ON': env.bool('FEATURE_ABOUT_UK_REGION_LISTING_PAGE_ENABLED', False),
    'CAPITAL_INVEST_OPPORTUNITY_PAGE_ON': env.bool('FEATURE_CAPITAL_INVEST_OPPORTUNITY_PAGE_ENABLED', False),
    'CAPITAL_INVEST_LANDING_PAGE_ON': env.bool('FEATURE_CAPITAL_INVEST_LANDING_PAGE_ENABLED', False),
    'CAPITAL_INVEST_OPPORTUNITY_LISTING_PAGE_ON': env.bool(
        'FEATURE_CAPITAL_INVEST_OPPORTUNITY_LISTING_PAGE_ENABLED', False
    ),
    'CAPITAL_INVEST_SUB_SECTOR_PAGE_ON': env.bool('FEATURE_CAPITAL_INVEST_SUB_SECTOR_PAGE_ENABLED', False),
    'CAPITAL_INVEST_CONTACT_FORM_PAGE_ON': env.bool('FEATURE_CAPITAL_INVEST_CONTACT_FORM_PAGE_ENABLED', False),
    'EXPAND_REDIRECT_ON': env.bool('FEATURE_EXPAND_REDIRECT_ENABLED', False),
    'NEW_IA_ON': env.bool('FEATURE_NEW_IA_ENABLED', False),
    'GUIDE_TO_BUSINESS_ENVIRONMENT_FORM_ON': env.bool('FEATURE_GUIDE_TO_BUSINESS_ENVIRONMENT_FORM_ENABLED', False),
    'INDUSTRIES_REDIRECT_ON': env.bool('FEATURE_INDUSTRIES_REDIRECT_ENABLED', False),
    'HOW_TO_SET_UP_REDIRECT_ON': env.bool('FEATURE_HOW_TO_SET_UP_REDIRECT_ENABLED', False),
    'ABOUT_UK_LANDING_PAGE_ON': env.bool('FEATURE_ABOUT_UK_LANDING_PAGE_ENABLED', False),
    'CAPITAL_INVEST_CONTACT_IN_TRIAGE_ON': env.bool('FEATURE_CAPITAL_INVEST_CONTACT_IN_TRIAGE_ENABLED', False),
    'EXPORTING_TO_UK_ON': env.bool('FEATURE_EXPORTING_TO_UK_ON_ENABLED', False),
    'INTERNATIONAL_TRIAGE_ON': env.bool('FEATURE_INTERNATIONAL_TRIAGE_ENABLED', False)
}

# Invest High Potential Opportunities
HPO_GOV_NOTIFY_AGENT_EMAIL_ADDRESS = env.str('HPO_GOV_NOTIFY_AGENT_EMAIL_ADDRESS',)
HPO_GOV_NOTIFY_AGENT_TEMPLATE_ID = env.str('HPO_GOV_NOTIFY_AGENT_TEMPLATE_ID', '064e2801-18f4-4342-a9e3-5eecddfa7d04')
HPO_GOV_NOTIFY_USER_TEMPLATE_ID = env.str('HPO_GOV_NOTIFY_USER_TEMPLATE_ID', 'a9285cb0-6acf-428f-94f7-2da7248d9ef0')

# Directory healthcheck
DIRECTORY_HEALTHCHECK_TOKEN = env.str('HEALTH_CHECK_TOKEN')
DIRECTORY_HEALTHCHECK_BACKENDS = [
    directory_healthcheck.backends.FormsAPIBackend,
    directory_healthcheck.backends.CMSAPIBackend,
    directory_healthcheck.backends.APIBackend,
    # health_check.cache.CacheBackend is also registered in
    # INSTALLED_APPS's health_check.cache
]


# PFP
PFP_API_CLIENT_API_KEY = env.str('PFP_API_CLIENT_API_KEY')
PFP_API_CLIENT_BASE_URL = env.str('PFP_API_CLIENT_BASE_URL')
PFP_API_CLIENT_SENDER_ID = 'directory'
PFP_API_CLIENT_DEFAULT_TIMEOUT = env.int('DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT', 2)
PFP_AWS_S3_PDF_STORE_ACCESS_KEY_ID = env.str('PFP_AWS_S3_PDF_STORE_ACCESS_KEY_ID')  # NOQA
PFP_AWS_S3_PDF_STORE_SECRET_ACCESS_KEY = env.str('PFP_AWS_S3_PDF_STORE_SECRET_ACCESS_KEY')  # NOQA
PFP_AWS_S3_PDF_STORE_BUCKET_NAME = env.str('PFP_AWS_S3_PDF_STORE_BUCKET_NAME')
PFP_AWS_S3_PDF_STORE_BUCKET_REGION = env.str('PFP_AWS_S3_PDF_STORE_BUCKET_REGION', 'eu-west-2')  # NOQA


# Sorl-thumbnail
THUMBNAIL_FORMAT = 'PNG'
THUMBNAIL_STORAGE_CLASS_NAME = env.str('THUMBNAIL_STORAGE_CLASS_NAME', 's3')
THUMBNAIL_KVSTORE_CLASS_NAME = env.str('THUMBNAIL_KVSTORE_CLASS_NAME', 'redis')
THUMBNAIL_STORAGE_CLASSES = {
    's3': 'storages.backends.s3boto3.S3Boto3Storage',
    'local-storage': 'django.core.files.storage.FileSystemStorage',
}
THUMBNAIL_KVSTORE_CLASSES = {
    'redis': 'sorl.thumbnail.kvstores.redis_kvstore.KVStore',
    'dummy': 'sorl.thumbnail.kvstores.dbm_kvstore.KVStore',
}
THUMBNAIL_DEBUG = DEBUG
THUMBNAIL_KVSTORE = THUMBNAIL_KVSTORE_CLASSES[THUMBNAIL_KVSTORE_CLASS_NAME]
THUMBNAIL_STORAGE = THUMBNAIL_STORAGE_CLASSES[THUMBNAIL_STORAGE_CLASS_NAME]
# Workaround for slow S3
# https://github.com/jazzband/sorl-thumbnail#is-so-slow-in-amazon-s3-
THUMBNAIL_FORCE_OVERWRITE = True

# Redis for thumbnails cache
if REDIS_URL:
    THUMBNAIL_REDIS_URL = REDIS_URL


INVEST_REDIRECTS_UNUSED_LANGUAGES = env.tuple('INVEST_REDIRECTS_UNUSED_LANGUAGES', default=('ar', 'ja'))

# Settings for email to supplier
CONTACT_SUPPLIER_SUBJECT = env.str('CONTACT_SUPPLIER_SUBJECT', 'Someone is interested in your Find a Buyer profile')
CONTACT_INDUSTRY_AGENT_EMAIL_ADDRESS = env.str('CONTACT_INDUSTRY_AGENT_EMAIL_ADDRESS')
CONTACT_INDUSTRY_AGENT_TEMPLATE_ID = env.str(
    'CONTACT_INDUSTRY_AGENT_TEMPLATE_ID', 'a9318bce-7d65-41b2-8d4c-b4a76ba285a2'
)
CONTACT_INDUSTRY_USER_TEMPLATE_ID = env.str(
    'CONTACT_INDUSTRY_USER_TEMPLATE_ID', '6a97f783-d246-42ca-be53-26faf3b08e32'
)
CONTACT_INDUSTRY_USER_REPLY_TO_ID = env.str('CONTACT_INDUSTRY_USER_REPLY_TO_ID', None)

CAPITAL_INVEST_AGENT_TEMPLATE_ID = env.str('CAPITAL_INVEST_AGENT_TEMPLATE_ID', '7d6e2bd5-f6a5-4050-9302-31bd033a2d8b')
CAPITAL_INVEST_USER_TEMPLATE_ID = env.str('CAPITAL_INVEST_USER_TEMPLATE_ID', '11cef6bd-c3e6-43c6-8959-f749f3991188')
# When none, default GOV.UK Notify reply-to email is used
CAPITAL_INVEST_USER_REPLY_TO_ID = env.str('CAPITAL_INVEST_USER_REPLY_TO_ID', None)

GUIDE_TO_UK_BUSINESS_ENVIRONMENT_USER_TEMPLATE_ID = env.str(
    'GUIDE_TO_UK_BUSINESS_ENVIRONMENT_USER_TEMPLATE_ID', 'e372134d-ffaa-44e8-abff-3ed6648485a5'
)
GUIDE_TO_UK_BUSINESS_ENVIRONMENT_AGENT_TEMPLATE_ID = env.str(
    'GUIDE_TO_UK_BUSINESS_ENVIRONMENT_AGENT_TEMPLATE_ID', '69d8223e-83a2-4a49-b35a-841278acd790'
)
GUIDE_TO_UK_BUSINESS_ENVIRONMENT_REPLY_TO_ID = env.str(
    'GUIDE_TO_UK_BUSINESS_ENVIRONMENT_REPLY_TO_ID', 'c071d4f6-94a7-4afd-9acb-6b164737731c'
)
HOW_WE_HELP_GUIDE_USER_TEMPLATE_ID = env.str(
    'HOW_WE_HELP_GUIDE_USER_TEMPLATE_ID', '683df2bf-56ab-4d74-a69f-b9556e76a4e8'
)
HOW_WE_HELP_GUIDE_AGENT_TEMPLATE_ID = env.str(
    'HOW_WE_HELP_GUIDE_AGENT_TEMPLATE_ID', 'c22f934b-b651-4d10-b8bb-65412f97ca3c'
)
HOW_WE_HELP_GUIDE_REPLY_TO_ID = env.str('HOW_WE_HELP_GUIDE_REPLY_TO_ID', 'd55f555c-354f-4988-8eba-6b9143d9015b')
GUIDE_TO_UK_BUSINESS_ENVIRONMENT_AGENT_EMAIL = env.str('GUIDE_TO_UK_BUSINESS_ENVIRONMENT_AGENT_EMAIL')
HOW_WE_HELP_GUIDE_AGENT_EMAIL = env.str('HOW_WE_HELP_GUIDE_AGENT_EMAIL')
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']
