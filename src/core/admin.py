from django.contrib import admin

from reading_statistics.models import ReadingStatistic
from reading_sessions.models import Session
from visitors.models import Visitor
from books.models import Book

admin.site.register(Visitor)
admin.site.register(Session)
admin.site.register(Book)
admin.site.register(ReadingStatistic)
