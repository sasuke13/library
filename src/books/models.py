from datetime import datetime, timedelta

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=32)
    author = models.CharField(max_length=50)
    year_of_publication = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(datetime.now().year)
        ]
    )
    short_about = models.CharField(max_length=128)
    about = models.CharField(max_length=512)
    last_used = models.DateTimeField(blank=True, null=True)
    total_reading_time = models.DurationField(default=timedelta(seconds=0))
