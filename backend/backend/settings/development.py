from base import *
import os
from dotenv import load_dotenv
load_dotenv(override=True)

USER = os.getenv("")
HOST = os.getenv("")
POART = os.getenv("")
DB = os.getenv("")
PASS = os.getenv("")


DEBUG = True
ALLOWED_HOSTS = ["*"]

CORS_ALLOW_ALL_ORIGINS: True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB,
        'USER': USER,
        'PASSWORD': PASS,
        'HOST': HOST,
        'PORT':POART,
    }
}