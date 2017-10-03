from django.contrib import admin
from . import models
from django.conf import settings
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
#admin.site.register(settings.AUTH_USER_MODEL) sounds good does not work...
# import Donald Trump Meme
