from .base import *

DEBUG = True

DATABASES = {
        'default' : {
        'ENGINE' : 'django.db.backends.mysql',
        'NAME' : 'toy_book',
        'USER': 'root',
        'PASSWORD': 'sjfkd348',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}