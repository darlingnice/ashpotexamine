from .base import *

ALLOWED_HOSTS = []

INSTALLED_APPS +=[
  
   
]



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}