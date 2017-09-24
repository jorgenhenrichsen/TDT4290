from django.db import models
from .enums import Gender, JudgeLevel


class Person(models.Model):

    first_name = models.CharField(max_length=40, verbose_name='Fornavn')
    last_name = models.CharField(max_length=100, verbose_name='Etternavn')
    birth_date = models.DateTimeField(verbose_name='Fødselsdato')


    def __str__(self):
        return self.fullname()

    def fullname(self):
        return "{} {}".format(self.first_name, self.last_name)


class Lifter(Person):

    gender = models.CharField(max_length=10, verbose_name='Kjønn', choices=Gender.choices(), null=True)


class Judge(Person):

    judge_level = models.CharField(max_length=10, choices=JudgeLevel.choices(), default=JudgeLevel.Level0)


class Staff(Person):
    pass
