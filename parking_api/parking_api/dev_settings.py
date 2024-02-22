# pylint: skip-file
# flake8: noqa

from .settings import *

from dotenv import load_dotenv

load_dotenv()

INSTALLED_APPS += (
    'django_extensions',
)
