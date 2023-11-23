from django.contrib import admin

from visitors.models import Visitor, Session
from books.models import Book

admin.site.register(Visitor)
admin.site.register(Session)
admin.site.register(Book)
