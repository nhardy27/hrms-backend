from .base import *
import os
from dotenv import load_dotenv
load_dotenv(override=True)

USER = os.getenv("S_USER")
HOST = os.getenv("S_HOST")
PORT = os.getenv("S_PORT")
DB = os.getenv("S_DB")
PASS = os.getenv("S_PASS")

DEBUG = False
ALLOWED_HOSTS = [ "https://placeholder-stage.humbingo.in"]

CORS_ALLOWED_ORIGINS = [ 
    "https://placeholder-stage.humbingo.in",
]

DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql',
         'NAME': DB,
         'HOST': HOST,
         'PORT': PORT,
         'USER':USER,
         'PASSWORD': PASS
     }
}

BASE_URL = os.getenv("BASE_URL")