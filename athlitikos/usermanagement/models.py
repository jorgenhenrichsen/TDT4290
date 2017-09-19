from django.db import models


class Person(models.Model):

    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateTimeField()


class Lifter(Person):
    pass
