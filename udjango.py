from datetime import datetime
import sys

import django
from django.apps import apps
from django.apps.config import AppConfig
from django.conf import settings
from django.core.management import color
from django.db import connection, models

NAME = 'udjango'


def main():
    setup()

    class Blog(models.Model):
        class Meta:
            app_label = NAME  # This line is needed for EVERY model
        name = models.CharField(max_length=100)
        tagline = models.TextField()

        def __str__(self):              # __unicode__ on Python 2
            return self.name

    class Author(models.Model):
        class Meta:
            app_label = NAME  # This line is needed for EVERY model
        name = models.CharField(max_length=50)
        email = models.EmailField()

        def __str__(self):              # __unicode__ on Python 2
            return self.name

    class Entry(models.Model):
        class Meta:
            app_label = NAME  # This line is needed for EVERY model
        blog = models.ForeignKey(Blog, related_name='entries')
        headline = models.CharField(max_length=255)
        body_text = models.TextField()
        pub_date = models.DateField()
        mod_date = models.DateField()
        authors = models.ManyToManyField(Author)
        n_comments = models.IntegerField()
        n_pingbacks = models.IntegerField()
        rating = models.IntegerField()

        def __str__(self):              # __unicode__ on Python 2
            return self.headline

    syncdb(Blog)
    syncdb(Author)
    syncdb(Entry)

    a = Author(name='Jimmy')
    a.save()
    b = Blog(name="Jimmy's Jottings")
    b.save()
    b2 = Blog(name="Joey's Jottings")
    b2.save()
    e = Entry(blog=b,
              headline='Hello, World!',
              pub_date=datetime.now(),
              mod_date=datetime.now(),
              n_comments=0,
              n_pingbacks=0,
              rating=3)
    e.save()
    assert e == b.entries.first()

    b3 = Blog.objects.get(entries__headline__contains='Hell')
    assert b == b3

    b4 = Blog.objects.get(entries__isnull=False)
    assert b == b4

    b5 = Blog.objects.get(entries__isnull=True)
    assert b2 == b5
    print('Done.')


def setup():
    DB_FILE = NAME + '.db'
    with open(DB_FILE, 'w'):
        pass  # wipe the database
    settings.configure(DEBUG=True,
                       DATABASES={
                            'default': {
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

    Based on https://code.djangoproject.com/wiki/DynamicModels#Syncdb
    """
    # disable terminal colors in the sql statements
    style = color.no_style()

    cursor = connection.cursor()
    statements, _pending = connection.creation.sql_create_model(model, style)
    for sql in statements:
        cursor.execute(sql)

main()
