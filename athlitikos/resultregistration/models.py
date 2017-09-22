from django.db import models
from .enums import Gender, JudgeLevel


# Create your models here.

class Competition(models.Model):
    # comeptitionArranger = models.ForeignKey(Organisation)
    competitionCategory = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    startDate = models.DateField()



class Group(models.Model):
    groupNumber = models.IntegerField()
    competition = models.ForeignKey(Competition)
    date = models.DateField()

    competitionLeader = models.ForeignKey('Staff', related_name='competitionLeader')
    jury = models.ManyToManyField('Staff', related_name='jury')
    judges = models.ManyToManyField('Judge', related_name='judges')
    secretary = models.ForeignKey('Staff', related_name='secretary')
    speaker = models.ForeignKey('Staff', related_name='speaker')
    technicalController = models.ForeignKey('Staff', related_name='technicalController')
    cheifMarshall = models.ForeignKey('Staff', related_name='chiefMarshall')
    timeKeeper = models.ForeignKey('Staff', related_name='timeKeeper')
    notes = models.CharField(max_length=300)
    recordsDescription = models.CharField(max_length=300)

    class Meta:
        unique_together = ('groupNumber', 'competition')

# Result for weightlifting(snatch/cleanAndJerk)
class Result(models.Model):
    resultID = models.IntegerField(primary_key=True)
    total = models.IntegerField()
    points = models.IntegerField()
    points_veteran = models.IntegerField()  # or some sort of logic?
    sinclair_coefficient = models.FloatField()  # or decimalField?
    best_snatch = models.ForeignKey('MoveAttempt', related_name='best_snatch', null=True)
    best_clean_and_jerk = models.ForeignKey('MoveAttempt', related_name='best_clean_and_jerk', null=True)
    group = models.ForeignKey(Group)
    lifter = models.ForeignKey('Lifter')


class MoveAttempt(models.Model):
    MOVE_TYPE_CHOICES = ((0, 'Snatch'), (1, 'Clean and jerk'))
    parentResult = models.ForeignKey('Result', on_delete=models.CASCADE)
    attemptNum = models.IntegerField()
    moveType = models.IntegerField(choices=MOVE_TYPE_CHOICES)
    weight = models.IntegerField()
    success = models.BooleanField()

    class Meta:
        unique_together = ('parentResult', 'attemptNum')


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
