"""Database settings for the Django project."""

import os
from urllib.parse import quote_plus

import environ
from mongoengine import connect

from core.settings.common import BASE_DIR

# Load environment variables from the .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Initialize environment variables
env = environ.Env(
    DATABASE_ENGINE=(str, "django.db.backends.sqlite3"),
    DATABASE_NAME=(str, os.path.join(BASE_DIR, "db.sqlite3")),
    DATABASE_USER=(str, ""),
    DATABASE_PASSWORD=(str, ""),
    DATABASE_HOST=(str, ""),
    DATABASE_PORT=(int, ""),
    MONGO_DATABASE_NAME=(str, "workflow_db"),
    MONGO_DATABASE_HOST=(str, "localhost"),  # Replace with the MongoDB host
    MONGO_DATABASE_PORT=(int, 27017),
    MONGO_DATABASE_USER=(str, ""),
    MONGO_DATABASE_PASSWORD=(str, ""),
)

# SQL Database settings (example with SQLite)
DATABASES = {
    "default": {
        "ENGINE": env("DATABASE_ENGINE"),
        "NAME": env("DATABASE_NAME"),
        "USER": env("DATABASE_USER"),
        "PASSWORD": env("DATABASE_PASSWORD"),
        "HOST": env("DATABASE_HOST"),
        "PORT": env("DATABASE_PORT"),
    },
}

# MongoDB connection settings
MONGO_DATABASE_NAME = env("MONGO_DATABASE_NAME")
MONGO_DATABASE_HOST = env("MONGO_DATABASE_HOST")
MONGO_DATABASE_PORT = env("MONGO_DATABASE_PORT")
MONGO_DATABASE_USER = env("MONGO_DATABASE_USER")
MONGO_DATABASE_PASSWORD = env("MONGO_DATABASE_PASSWORD")

# URL-encode the username and password
MONGO_DATABASE_USER = quote_plus(MONGO_DATABASE_USER)
MONGO_DATABASE_PASSWORD = quote_plus(MONGO_DATABASE_PASSWORD)

# Build the MongoDB URI
if MONGO_DATABASE_USER and MONGO_DATABASE_PASSWORD:
    MONGO_URI = (
        f"mongodb://{MONGO_DATABASE_USER}:{MONGO_DATABASE_PASSWORD}@"
        f"{MONGO_DATABASE_HOST}:{MONGO_DATABASE_PORT}/"
        f"{MONGO_DATABASE_NAME}"
    )
else:
    MONGO_URI = (
        f"mongodb://{MONGO_DATABASE_HOST}:{MONGO_DATABASE_PORT}/{MONGO_DATABASE_NAME}"
    )

try:
    connect(MONGO_DATABASE_NAME, host=MONGO_URI, serverSelectionTimeoutMS=3000)
except Exception as e:
    print(f"⚠️ MongoDB connection failed: {e}")
