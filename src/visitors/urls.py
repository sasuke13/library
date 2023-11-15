from django.urls import path

from visitors.views import LogoutView, CookieTokenObtainPairView, CookieTokenRefreshView, VisitorApiView

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='visitor_logout'),
    path('login/', CookieTokenObtainPairView.as_view(), name='visitor_login'),
    path('refresh/', CookieTokenRefreshView.as_view(), name='visitor_refresh_token'),
    path('registration/', VisitorApiView.as_view(), name='visitor_registration')
]
