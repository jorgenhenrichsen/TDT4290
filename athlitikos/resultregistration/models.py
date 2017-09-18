from django.db import models

# Create your models here.

class Result(models.Model):
    resultID = models.IntegerField(primary_key=True)
    total = models.IntegerField()
    points = models.IntegerField()
    points_veteran = models.IntegerField()
