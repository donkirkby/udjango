# Tested with Django 1.11.15 and Python 3.6.
import logging
import sys

import django
from django.apps import apps
from django.apps.config import AppConfig
from django.conf import settings
from django.db import connections, models, DEFAULT_DB_ALIAS
from django.db.models.base import ModelBase

NAME = 'udjango'
DB_FILE = NAME + '.db'


def main():
    setup()
    logger = logging.getLogger(__name__)

    class Person(models.Model):
        first_name = models.CharField(max_length=30)
        last_name = models.CharField(max_length=30)

    syncdb(Person)

    p1 = Person(first_name='Jimmy', last_name='Jones')
    p1.save()
    p2 = Person(first_name='Bob', last_name='Brown')
    p2.save()

    logger.info(', '.join([p.first_name for p in Person.objects.all()]))


def setup():
    with open(DB_FILE, 'w'):
        pass  # wipe the database
    settings.configure(
        DEBUG=True,
        DATABASES={
            DEFAULT_DB_ALIAS: {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': DB_FILE}},
        LOGGING={'version': 1,
                 'disable_existing_loggers': False,
                 'formatters': {
                    'debug': {
                        'format': '%(asctime)s[%(levelname)s]'
                                  '%(name)s.%(funcName)s(): %(message)s',
                        'datefmt': '%Y-%m-%d %H:%M:%S'}},
                 'handlers': {
                    'console': {
                        'level': 'DEBUG',
                        'class': 'logging.StreamHandler',
                        'formatter': 'debug'}},
                 'root': {
                    'handlers': ['console'],
                    'level': 'INFO'},
                 'loggers': {
                    "django.db": {"level": "DEBUG"}}})
    app_config = AppConfig(NAME, sys.modules['__main__'])
    apps.populate([app_config])
    django.setup()
    original_new_func = ModelBase.__new__

    @staticmethod
    def patched_new(cls, name, bases, attrs):
        if 'Meta' not in attrs:
            class Meta:
                app_label = NAME
            attrs['Meta'] = Meta
        return original_new_func(cls, name, bases, attrs)
    ModelBase.__new__ = patched_new


def syncdb(model):
    """ Standard syncdb expects models to be in reliable locations.

    Based on https://github.com/django/django/blob/1.9.3
    /django/core/management/commands/migrate.py#L285
    """
    connection = connections[DEFAULT_DB_ALIAS]
    with connection.schema_editor() as editor:
        editor.create_model(model)


main()
