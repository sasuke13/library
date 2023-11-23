from django.urls import path

from visitors.views import (
    LogoutView, CookieTokenObtainPairView, CookieTokenRefreshView, VisitorRegistrationApiView,
    SessionAPIView, CloseSessionAPIView
)

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='visitor_logout'),
    path('login/', CookieTokenObtainPairView.as_view(), name='visitor_login'),
    path('refresh/', CookieTokenRefreshView.as_view(), name='visitor_refresh_token'),
    path('registration/', VisitorRegistrationApiView.as_view(), name='visitor_registration'),
    path('open_session/<int:book_id>/', SessionAPIView.as_view(), name='open_session'),
    path('current_session/', SessionAPIView.as_view(), name='current_session'),
    path('current_session/close/', CloseSessionAPIView.as_view(), name='close_current_session')
]
