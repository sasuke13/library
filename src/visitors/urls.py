from django.urls import path

from visitors.views import (
    LogoutView, CookieTokenObtainPairView, CookieTokenRefreshView, VisitorRegistrationApiView
)

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='visitor_logout'),
    path('login/', CookieTokenObtainPairView.as_view(), name='visitor_login'),
    path('refresh/', CookieTokenRefreshView.as_view(), name='visitor_refresh_token'),
    path('registration/', VisitorRegistrationApiView.as_view(), name='visitor_registration'),
]
