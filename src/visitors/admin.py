from django.contrib import admin

from . import models

admin.site.register(models.Visitor)
admin.site.register(models.Session)
admin.site.register(models.ReadingStatistic)
admin.site.register(models.Book)
