from django.urls import path

from reading_statistics.views import StatisticsAPIView, VisitorStatisticsAPIView

urlpatterns = [
    path('', StatisticsAPIView.as_view(), name='get_all_statistics'),
    path('visitor/', VisitorStatisticsAPIView.as_view(), name='get_all_statistics_by_user'),
    path(
        'visitor/books/<int:book_id>/',
        VisitorStatisticsAPIView.as_view(),
        name='get_user_statistics_by_user_and_book'
    ),
    path('books_statistics/<int:book_id>/', StatisticsAPIView.as_view(), name='get_all_statistics_by_book'),
]
