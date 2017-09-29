from django.db import models
from .enums import Gender, JudgeLevel
from .validators import validate_name
#from datetime import datetime
#from django.db.models.signals import pre_save is usefull ;)


# Create your models here.

class Competition(models.Model):
    # comeptitionArranger = models.ForeignKey(Organisation)
    competitionCategory = models.CharField(max_length=100,validators=[validate_name])
    location = models.CharField(max_length=100)
    startDate = models.DateField(help_text="år-måned-dag")

    def __str__(self):
        return '{0}, {1}, {2}'.format(self.competitionCategory, self.location, self.startDate)

class Club(models.Model):
    clubName = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    models.ManyToManyField(Competition, null=True) #One Club can join many competitions

    def __str__(self):
        return self.clubName


class Group(models.Model):
    #   Identifying
    groupNumber = models.IntegerField()
    competition = models.ForeignKey(Competition)
    date = models.DateField()

    competitors = models.ForeignKey('Lifter', null=True)

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

    def __str__(self):
        return '{0}, group {1}, {2}'.format(self.competition, self.groupNumber, self.date)

    class Meta:
        unique_together = ('groupNumber', 'competition')

# Result for weightlifting(snatch/cleanAndJerk)
class Result(models.Model):
    resultID = models.IntegerField(primary_key=True)

    #   These should be made into derived properties based on the MoveAttempts that this result consists of
    total = models.IntegerField(null=True)
    points = models.IntegerField(null=True)

    #   These should be made into derived properties based on the age/weight of the lifter, as well as the points
    points_veteran = models.IntegerField(null=True)
    sinclair_coefficient = models.FloatField(null=True)  # or decimalField?

    #   Should be derived from the best snatch and clean_and_jerk MoveAttempts respectively
    best_snatch = models.ForeignKey('MoveAttempt', related_name='best_snatch', null=True)
    best_clean_and_jerk = models.ForeignKey('MoveAttempt', related_name='best_clean_and_jerk', null=True)

    group = models.ForeignKey(Group, null=True)     # The Group that this result belongs to.
    lifter = models.ForeignKey('Lifter')    # The Lifter that this result belongs to


class MoveAttempt(models.Model):
    # Currently only made for the lifting attempts, not the pentathlon

    MOVE_TYPE_CHOICES = ((0, 'Snatch'), (1, 'Clean and jerk'))
    parentResult = models.ForeignKey('Result', on_delete=models.CASCADE)    # The Result this is part of
    moveType = models.IntegerField(choices=MOVE_TYPE_CHOICES)
    attemptNum = models.IntegerField()
    weight = models.IntegerField()  # Weight that was attempted lifted
    success = models.BooleanField()

    def __str__(self):
        return '{0}, attempt {1}, weight {2}, {3}'.format(self.moveType, self.attemptNum, self.weight, self.success)

    class Meta:
        # The MoveAttempt should be uniquely identified
        # by a combination of the result it belongs to, the attempt number and the moveType
        unique_together = ('parentResult', 'attemptNum')


class Person(models.Model):

    first_name = models.CharField(max_length=40, verbose_name='Fornavn', validators=[validate_name])
    last_name = models.CharField(max_length=100, verbose_name='Etternavn', validators=[validate_name])
    birth_date = models.DateField(verbose_name='Fødselsdato')   # Changed from dateTime, as we don't need time of birth


    def __str__(self):
        return self.fullname()

    def fullname(self):
        return "{} {}".format(self.first_name, self.last_name)


class Lifter(Person):

    gender = models.CharField(max_length=10, verbose_name='Kjønn', choices=Gender.choices(), null=True)
    club = models.ForeignKey('Club', null=True)  # The club that this lifter< belongs to


class Judge(Person):

    judge_level = models.CharField(max_length=10, choices=JudgeLevel.choices(), default=JudgeLevel.Level0)




class Staff(Person):
    pass
