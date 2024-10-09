from .base import *


ALLOWED_HOSTS =  ['127.0.0.1','.pythonanywhere.com','digitalocean.com']

INSTALLED_APPS +=[
   'utilitities',
   'tokens_app'


]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ashpotexamine',
        'USER': 'lyntonjay',
        'PASSWORD': '30042020',
        'HOST': 'localhost',  
        'PORT': '',  # Default port  5432
    }
}


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


from ashpotexamine.config.settings.email_sending import *