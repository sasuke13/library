from django.urls import path

from books.views import BookAPIVew

urlpatterns = [
    path('', BookAPIVew.as_view(), name='get_all_books'),
    path('<int:book_id>/', BookAPIVew.as_view(), name='books_detailed_view'),
]
