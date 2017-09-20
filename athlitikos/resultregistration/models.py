from django.db import models
from enum import Enum
import inspect


class ChoiceEnum(Enum):

    @classmethod
    def choices(cls):
        members = inspect.getmembers(cls, lambda m: not(inspect.isroutine(m)))
        properties = [m for m in members if not(m[0][:2] == '__')]
        choices = tuple([(str(p[1].value), p[0]) for p in properties])
        return choices


class JudgeLevel(ChoiceEnum):
    Level0 = 0
    Level1 = 1
    Level2 = 2
    Level3 = 3


class Gender(ChoiceEnum):
    male = 'M'
    female = 'K'


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
