from django.urls import path

from visitors.views import LogoutView, CookieTokenObtainPairView, CookieTokenRefreshView, VisitorRegistrationApiView, \
     SessionAPIView, CloseSessionAPIView, StatisticsAPIView, VisitorStatisticsAPIView

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='visitor_logout'),
    path('login/', CookieTokenObtainPairView.as_view(), name='visitor_login'),
    path('refresh/', CookieTokenRefreshView.as_view(), name='visitor_refresh_token'),
    path('registration/', VisitorRegistrationApiView.as_view(), name='visitor_registration'),
    path('global_statistic/', StatisticsAPIView.as_view(), name='get_all_statistics'),
    path('statistic/', VisitorStatisticsAPIView.as_view(), name='get_all_statistics_by_user'),
    path('books/statistic/<int:book_id>/', VisitorStatisticsAPIView.as_view(), name='get_user_statistics_by_book'),
    path('statistic/books/<int:book_id>/', StatisticsAPIView.as_view(), name='get_all_statistics_by_book'),
    path('open_session/<int:book_id>/', SessionAPIView.as_view(), name='open_session'),
    path('current_session/', SessionAPIView.as_view(), name='current_session'),
    path('current_session/close/', CloseSessionAPIView.as_view(), name='close_current_session')
]
