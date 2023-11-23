from django.db import models


class Session(models.Model):
    book = models.ForeignKey(to='books.Book', related_name='sessions', null=True, on_delete=models.SET_NULL)
    visitor = models.ForeignKey(to='visitors.Visitor', related_name='sessions', on_delete=models.CASCADE)
    session_start = models.DateTimeField(auto_now_add=True)
    session_end = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)
