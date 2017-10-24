from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Person)
admin.site.register(models.Lifter)
admin.site.register(models.Judge)
admin.site.register(models.Staff)
admin.site.register(models.Competition)
admin.site.register(models.Group)
admin.site.register(models.Result)
admin.site.register(models.MoveAttempt)
admin.site.register(models.Club)
admin.site.register(models.PentathlonResult)
admin.site.register(models.InternationalResult)
admin.site.register(models.InternationalLifter)
