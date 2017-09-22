from django.db import models

# Create your models here.
MOVE_TYPE_CHOICES = ((0,'Snatch'), (1,'Clean and jerk'))


class Competition(models.Model):
    # comeptitionArranger = models.ForeignKey(Organisation)
    competitionCategory = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    startDate = models.DateField()



class Group(models.Model):
    groupNumber = models.IntegerField()
    competition = models.ForeignKey(Competition)
    date = models.DateField()

    # competitionLeader = models.ForeignKey(Person)
    # jury many to one?
    # judge many to one?
    # secretary = models.ForeignKey(Person)
    # speaker = models.ForeignKey(Person)
    # technicalController = models.ForeignKey(Person)
    # cheifMarshall = models.ForeignKey(Person)
    # timeKeeper = models.ForeignKey(Person)
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

    #   Why will this not work?
    best_snatch = models.ForeignKey('MoveAttempt', related_name='best_snatch', null=True)
    best_clean_and_jerk = models.ForeignKey('MoveAttempt', related_name='best_clean_and_jerk', null=True)

    group = models.ForeignKey(Group)
    # person = models.ForeignKey(Lifter)


class MoveAttempt(models.Model):
    parentResult = models.ForeignKey('Result', on_delete=models.CASCADE)
    attemptNum = models.IntegerField()
    moveType = models.IntegerField(choices=MOVE_TYPE_CHOICES)
    weight = models.IntegerField()
    success = models.BooleanField()

    class Meta:
        unique_together = ('parentResult', 'attemptNum')


# moveType = models.IntegerField(choices=MOVE_TYPES)
# class MoveType(models.Model):
#     moveTypeName = models.CharField(max_length=75, primary_key=True)
#     moveTypeDescription = models.CharField(max_length=100)

# class MoveAttempt(models.Model):
#     moveType = models.ForeignKey(MoveType)
#     moveName = models.IntegerField(choices=MOVE_TYPES)

# stevne, person, resultat

