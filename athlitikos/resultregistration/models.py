from django.db import models

# Create your models here.

class Result(models.Model):
    resultID = models.IntegerField(primary_key=True)
    total = models.IntegerField()
    points = models.IntegerField()
    points_veteran = models.IntegerField()
    sinclair_coefficient = models.FloatField()
    best_snatch = models.IntegerField()
    best_clean_and_jerk = models.IntegerField()
    #lifter = models.ForeignKey(Person)



