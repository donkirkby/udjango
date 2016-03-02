# Tested with Django 1.9.2
import sys

import django
from django.apps import apps
from django.apps.config import AppConfig
from django.conf import settings
from django.db import connections, models, DEFAULT_DB_ALIAS

NAME = 'udjango'


def main():
    setup()

    class Person(models.Model):
        class Meta:
            app_label = NAME  # This line is needed for EVERY model

        first_name = models.CharField(max_length=30)
        last_name = models.CharField(max_length=30)

    syncdb(Person)

    p1 = Person(first_name='Jimmy', last_name='Jones')
    p1.save()
    p2 = Person(first_name='Bob', last_name='Brown')
    p2.save()

    print ', '.join([p.first_name for p in Person.objects.all()])


def setup():
    DB_FILE = NAME + '.db'
    with open(DB_FILE, 'w'):
        pass  # wipe the database
    settings.configure(DEBUG=True,
                       DATABASES={
                            DEFAULT_DB_ALIAS: {
                                'ENGINE': 'django.db.backends.sqlite3',
                                'NAME': DB_FILE}},
                       LOGGING={'version': 1,
                                'disable_existing_loggers': False,
                                'formatters': {
                                    'debug': {
                                        'format': '%(asctime)s[%(levelname)s]%(name)s.%(funcName)s(): %(message)s',
                                        'datefmt': '%Y-%m-%d %H:%M:%S'}},
                                'handlers': {
                                    'console': {
                                        'level': 'DEBUG',
                                        'class': 'logging.StreamHandler',
                                        'formatter': 'debug'}},
                                'root': {
                                    'handlers': ['console'],
                                    'level': 'WARN'},
                                'loggers': {
                                    "django.db": {"level": "WARN"}}})
    app_config = AppConfig(NAME, sys.modules['__main__'])
    apps.populate([app_config])
    django.setup()


def syncdb(model):
    """ Standard syncdb expects models to be in reliable locations.

    Based on https://github.com/django/django/blob/1.9.3/django/core/management/commands/migrate.py#L285
    """
    connection = connections[DEFAULT_DB_ALIAS]
    with connection.schema_editor() as editor:
        editor.create_model(model)

main()
