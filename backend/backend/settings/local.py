from .base import *
import os
from dotenv import load_dotenv
load_dotenv(override=True)

USER = os.getenv("L_USER")
HOST = os.getenv("L_HOST")
PORT = os.getenv("L_PORT")
DB = os.getenv("L_DB")
PASS = os.getenv("L_PASS")

DEBUG = True
ALLOWED_HOSTS = ["*"]

CORS_ALLOWED_ORIGINS = [ 
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB,
        'USER': USER,
        'PASSWORD': PASS,
        'HOST': HOST,
        'PORT':PORT,
    }
}

BASE_URL = 'http://127.0.0.1:8001/'