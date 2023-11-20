from django.contrib import admin

from visitors.models import Visitor, ReadingStatistic, Session
from books.models import Book

admin.site.register(Visitor)
admin.site.register(Session)
admin.site.register(ReadingStatistic)
admin.site.register(Book)
