from .base import *
import os
from dotenv import load_dotenv
load_dotenv(override=True)

USER = os.getenv("L_USER")
HOST = os.getenv("L_HOST")
POART = os.getenv("L_PORT")
DB = os.getenv("L_DB")
PASS = os.getenv("L_PASS")


DEBUG = True
ALLOWED_HOSTS = ["*"]


CORS_ALLOW_ALL_ORIGINS: True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

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