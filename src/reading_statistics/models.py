from datetime import timedelta

from django.db import models


class ReadingStatistic(models.Model):
    book = models.ForeignKey(to='books.Book', related_name='statistics', null=True, on_delete=models.SET_NULL)
    visitor = models.ForeignKey(to='visitors.Visitor', related_name='statistics', on_delete=models.CASCADE)
    total_reading_time = models.DurationField(default=timedelta(seconds=0))
