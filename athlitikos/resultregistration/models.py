from django.db import models

# Create your models here.
MOVE_TYPES = ((0,_('Snatch')),(1,_('Clean and jerk')))

#Result for weightlifting(snatch/cleanAndJerk)
class Result(models.Model):
    resultID = models.IntegerField(primary_key=True)
    total = models.IntegerField()
    points = models.IntegerField()
    points_veteran = models.IntegerField() #or some sort of logic?
    sinclair_coefficient = models.FloatField() #or decimalfield?
    best_snatch = models.ForeignKey(MoveAttempt)
    best_clean_and_jerk = models.ForeignKey(MoveAttempt)
    group = models.ForeignKey(Group)
    # person = models.ForeignKey(Lifter)


class MoveAttempt(models.Model):
    moveType = models.IntegerField(choices=MOVE_TYPES)
    weight = models.IntegerField()
    success = models.BooleanField()
    result = models.ForeignKey(Result)

    class Meta:
        unique_together = ('result', 'success', 'weight', 'moveType')


# moveType = models.IntegerField(choices=MOVE_TYPES)
# class MoveType(models.Model):
#     moveTypeName = models.CharField(max_length=75, primary_key=True)
#     moveTypeDescription = models.CharField(max_length=100)

# class MoveAttempt(models.Model):
#     moveType = models.ForeignKey(MoveType)
#     moveName = models.IntegerField(choices=MOVE_TYPES)

# stevne, person, resultat

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
