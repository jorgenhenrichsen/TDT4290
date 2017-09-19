from django.db import models


class Person(models.Model):

    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateTimeField()

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Lifter(Person):
    pass
