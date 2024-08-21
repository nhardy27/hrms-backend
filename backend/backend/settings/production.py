from .base import *
import os
from dotenv import load_dotenv
load_dotenv(override=True)

USER = os.getenv("P_USER")
HOST = os.getenv("P_HOST")
PORT = os.getenv("P_PORT")
DB = os.getenv("P_DB")
PASS = os.getenv("P_PASS")

DEBUG = False
ALLOWED_HOSTS = [ "https://placeholder.humbingo.in"]

CORS_ALLOWED_ORIGINS = [ 
    "https://placeholder.humbingo.in",
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