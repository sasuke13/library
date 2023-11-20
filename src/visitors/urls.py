from django.urls import path

from visitors.views import LogoutView, CookieTokenObtainPairView, CookieTokenRefreshView, VisitorRegistrationApiView, \
    VisitorStatisticAPIView, SessionAPIView, CloseSessionAPIView, StatisticsAPIView

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='visitor_logout'),
    path('login/', CookieTokenObtainPairView.as_view(), name='visitor_login'),
    path('refresh/', CookieTokenRefreshView.as_view(), name='visitor_refresh_token'),
    path('registration/', VisitorRegistrationApiView.as_view(), name='visitor_registration'),
    path('visitor/statistick/', VisitorStatisticAPIView.as_view(), name='get_user_statistic'),
    path('statistick/', StatisticsAPIView.as_view(), name='get_all_statistic'),
    path('book/statistick/<int:book_id>/', StatisticsAPIView.as_view(), name='get_all_statistic'),
    path('open_session/<int:book_id>/', SessionAPIView.as_view(), name='open_session'),
    path('current_session/', SessionAPIView.as_view(), name='current_session'),
    path('current_session/close/', CloseSessionAPIView.as_view(), name='close_current_session')
]
