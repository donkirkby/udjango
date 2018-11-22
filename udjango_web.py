#!/usr/bin/env python
# -*- coding:utf-8 -*-

""" A Django web app in a single file.

Based on Nsukami's blog post:
https://mlvin.xyz/django-single-file-project.html

To get it running, copy it into a directory named udjango:
$ pip install django
$ python udjango_web.py makemigrations udjango
$ python udjango_web.py migrate
$ python udjango_web.py createsuperuser
$ python udjango_web.py runserver

Then browse to http://localhost:8000/admin and log in with the user you created.
Add some authors and books, then browse to http://localhost:8000/api

Tested with Django 1.11.15 and Python 3.6.
"""


import os
import sys

import django
from django.conf import settings
from django.db import models
from django.contrib import admin
from django.conf.urls import url, include
from django.db.models.base import ModelBase
from django.http import HttpResponse
from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, 'udjango.db')

# the current folder name will also be our app
APP_LABEL = os.path.basename(BASE_DIR)
urlpatterns = []


def main():
    setup()

    from rest_framework import routers
    from rest_framework import serializers
    from rest_framework import viewsets

    # Create your models here.
    class Author(models.Model):
        name = models.CharField(max_length=200)

        def __str__(self):
            return self.name

    class Book(models.Model):
        author = models.ForeignKey(Author, related_name='books')
        title = models.CharField(max_length=400)

        def __str__(self):
            return self.title

    admin.site.register(Book)
    admin.site.register(Author)
    admin.autodiscover()

    class BookSerializer(serializers.ModelSerializer):
        class Meta:
            model = Book
            fields = '__all__'

    class BooksViewSet(viewsets.ReadOnlyModelViewSet):
        queryset = Book.objects.all()
        serializer_class = BookSerializer

    router = routers.DefaultRouter()
    router.register(r'books', BooksViewSet)

    def index(request):
        return HttpResponse(
            "Hello, Django! <a href='admin'>Web</a> or <a href='api'>API</a>?")

    urlpatterns.extend([
        url(r'^admin/', admin.site.urls),
        url(r'^$', index, name='homepage'),
        url(r'^api/', include(router.urls)),
        url(r'^api-auth/', include('rest_framework.urls',
                                   namespace='rest_framework'))
    ])

    if __name__ == "__main__":
        execute_from_command_line(sys.argv)
    else:
        get_wsgi_application()


def setup():
    sys.path[0] = os.path.dirname(BASE_DIR)

    settings.configure(
        DEBUG=True,
        ROOT_URLCONF=__name__,
        MIDDLEWARE=[
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
            'django.middleware.locale.LocaleMiddleware',
            ],
        INSTALLED_APPS=[
            APP_LABEL,
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'rest_framework',
            ],
        STATIC_URL='/static/',
        STATICFILES_DIRS=[
            os.path.join(BASE_DIR, "static"),
        ],
        STATIC_ROOT=os.path.join(BASE_DIR, "static_root"),
        MEDIA_ROOT=os.path.join(BASE_DIR, "media"),
        MEDIA_URL='/media/',
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [os.path.join(BASE_DIR, "templates")],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.debug',
                        'django.template.context_processors.i18n',
                        'django.template.context_processors.request',
                        'django.contrib.auth.context_processors.auth',
                        'django.template.context_processors.tz',
                        'django.contrib.messages.context_processors.messages',
                    ],
                },
            },
            ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': DB_FILE,
                }
            },
        REST_FRAMEWORK={
            'DEFAULT_PERMISSION_CLASSES': [
                'rest_framework.permissions.IsAdminUser',
            ],
        }
    )

    django.setup()
    original_new_func = ModelBase.__new__

    @staticmethod
    def patched_new(cls, name, bases, attrs):
        if 'Meta' not in attrs:
            class Meta:
                app_label = APP_LABEL
            attrs['Meta'] = Meta
        return original_new_func(cls, name, bases, attrs)
    ModelBase.__new__ = patched_new


main()
