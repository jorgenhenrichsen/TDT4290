from django.db import models

class Person(models.Model):

    first_name = models.CharField(max_length=40, verbose_name='Fornavn')
    last_name = models.CharField(max_length=100, verbose_name='Etternavn')