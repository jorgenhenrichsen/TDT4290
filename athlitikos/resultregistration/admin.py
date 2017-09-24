from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Person)
admin.site.register(models.Lifter)
admin.site.register(models.Judge)
admin.site.register(models.Staff)
