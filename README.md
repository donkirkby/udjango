This is a minimal, but runnable Django app called 𝜇Django.

[![Build Status]][travis-ci.org]

My goal was to create a runnable Django snippet that included a model.

I found several useful resources, but most no longer work under Django 1.11:

* a related discussion on [Stack Overflow][so]
* the Django wiki article on [dynamic models][wiki]
* [mini_django.py gist][gist] based on a [blog post][blog] about running Django
    in one file
* posts on Django in one file that just don't include models:
    [Olifante][olifante] and [software maniacs][maniacs]

Later, I found Nsukami's blog post (no longer on line) that included a web server, so I merged in those features and automated the migrations.

[so]: http://stackoverflow.com/q/1297873/4794
[wiki]: https://code.djangoproject.com/wiki/DynamicModels#Syncdb
[gist]: https://gist.github.com/k4ml/2219751
[blog]: http://fahhem.com/blog/2011/10/django-models-without-apps-or-everything-django-truly-in-a-single-file/
[olifante]: http://olifante.blogs.com/covil/2010/04/minimal-django.html
[maniacs]: http://softwaremaniacs.org/blog/2011/01/07/django-micro-framework/en/
[Build Status]: https://travis-ci.org/donkirkby/udjango.svg?branch=master
[travis-ci.org]: https://travis-ci.org/donkirkby/udjango
