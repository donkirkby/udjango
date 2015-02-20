import django
from django.conf import settings
from django.core.management import color
from django.db import connection, models

NAME = 'udjango'

def main():
    setup()
    
    class Person(models.Model):
        class Meta:
            app_label = NAME
            
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
    settings.configure(DEBUG=True,
                       DATABASES = {
                            'default': {
                                'ENGINE': 'django.db.backends.sqlite3',
                                'NAME': DB_FILE
                            }
                        })
    django.setup()
    with open(DB_FILE, 'w'): pass # wipe the database
    
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
