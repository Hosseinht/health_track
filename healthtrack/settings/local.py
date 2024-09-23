from os import getenv

from .base import *  # noqa
from .base import BASE_DIR

load_dotenv(env_file)

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]
SECRET_KEY = getenv("SECRET_KEY")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": getenv("POSTGRES_DB"),
        "USER": getenv("POSTGRES_USER"),
        "PASSWORD": getenv("POSTGRES_PASSWORD"),
        "HOST": getenv("POSTGRES_HOST"),
        "PORT": 5432,
    }
}
