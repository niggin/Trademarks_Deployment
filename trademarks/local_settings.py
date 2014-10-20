#Put all settings related to your current configuration right here
#settings.py must contain only global settings that applies to all configurations

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'trademarks',
        'USER': 'trademarks_user',
        'PASSWORD': '628802',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
