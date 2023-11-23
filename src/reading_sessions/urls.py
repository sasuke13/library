from django.urls import path

from reading_sessions.views import SessionAPIView, CloseSessionAPIView

urlpatterns = [
    path('open_session/<int:book_id>/', SessionAPIView.as_view(), name='open_session'),
    path('current_session/', SessionAPIView.as_view(), name='current_session'),
    path('current_session/close/', CloseSessionAPIView.as_view(), name='close_current_session')
]
