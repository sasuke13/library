from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from books.exceptions import BookDoesNotExist
from core.base_api import ApiBaseView
from core.containers import VisitorContainer, SessionContainer, ReadingStatisticContainer
from visitors.dto import VisitorRegistrationDTO
from visitors.exceptions import PasswordIsInvalid, SessionDoesNotExist, VisitorAlreadyExists, BookIsAlreadyTaken
from visitors.serializers import CookieTokenRefreshSerializer, ReadingStatisticDTOSerializer, VisitorDTOSerializer, \
    VisitorRegistrationDTOSerializer, SessionDTOSerializer


def logout(request, message: str):
    refresh_token = request.COOKIES.get("refresh_token")
    if refresh_token:
        token = RefreshToken(refresh_token)
        token.blacklist()

        response = Response(
            {"message": message},
            status=status.HTTP_200_OK
        )
        response.delete_cookie(
            "refresh_token",
            samesite=settings.COOKIE_SAME_SITE
        )
        return response

    return Response("Refresh token not found", status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        message = "User was successfully logged out"
        try:
            return logout(request, message)
        except TokenError as exception:
            return Response({"error": exception.args}, status=status.HTTP_400_BAD_REQUEST)


class CookieTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            response.set_cookie(
                "refresh_token",
                response.data["refresh"],
                max_age=settings.COOKIE_MAX_AGE,
                httponly=settings.COOKIE_HTTPONLY,
                secure=settings.COOKIE_SECURE,
                samesite=settings.COOKIE_SAME_SITE,
            )
            del response.data["refresh"]

        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)

    serializer_class = CookieTokenRefreshSerializer


class VisitorRegistrationApiView(APIView, ApiBaseView):
    visitor_interactor = VisitorContainer.interactor()

    def post(self, request):
        visitor_serializer = VisitorRegistrationDTOSerializer(data=request.data)

        is_visitor_serializer_valid = visitor_serializer.is_valid()

        if not is_visitor_serializer_valid:
            return self._create_response_for_invalid_serializers(visitor_serializer)

        visitor_dto = VisitorRegistrationDTO(**visitor_serializer.validated_data)

        try:
            created_visitor = self.visitor_interactor.registration(visitor_dto)
        except (PasswordIsInvalid, VisitorAlreadyExists) as exception:
            return self._create_response_for_exception(exception)

        serialized_created_visitor = VisitorDTOSerializer(created_visitor)

        return Response({'created_user': serialized_created_visitor.data}, status=status.HTTP_201_CREATED)


class SessionAPIView(APIView, ApiBaseView):
    permission_classes = [IsAuthenticated]

    session_interactor = SessionContainer.interactor()

    def get(self, request):
        try:
            session = self.session_interactor.get_active_session_dto_by_visitor(request.user)
        except SessionDoesNotExist as exception:
            return self._create_response_for_exception(exception)

        serialized_session = SessionDTOSerializer(session)

        return Response({'session': serialized_session.data}, status=status.HTTP_200_OK)

    def post(self, request, book_id: int):
        try:
            session = self.session_interactor.open_session(self.request.user, book_id)

        except (BookDoesNotExist, BookIsAlreadyTaken) as exception:
            return self._create_response_for_exception(exception)

        serialized_session = SessionDTOSerializer(session)

        return Response({
            'message': 'Session has been successfully opened!',
            'session': serialized_session.data
        }, status=status.HTTP_201_CREATED)


class CloseSessionAPIView(APIView, ApiBaseView):
    permission_classes = [IsAuthenticated]

    session_interactor = SessionContainer.interactor()

    def post(self, request):
        try:
            message = self.session_interactor.close_session(request.user)
        except SessionDoesNotExist as exception:
            return self._create_response_for_exception(exception)

        return Response({'message': message}, status=status.HTTP_200_OK)


class VisitorStatisticAPIView(APIView, ApiBaseView):
    permission_classes = [IsAuthenticated]

    reading_statistic_interactor = ReadingStatisticContainer.interactor()

    def get(self, request):
        statistics = self.reading_statistic_interactor.get_all_statistics_dto_by_visitor(request.user)

        serialized_statistics = ReadingStatisticDTOSerializer(statistics, many=True)

        return Response({'statistic': serialized_statistics.data}, status=status.HTTP_201_CREATED)


class StatisticsAPIView(APIView, ApiBaseView):
    reading_statistic_interactor = ReadingStatisticContainer.interactor()

    def get(self, request, book_id: int = None):
        if book_id:
            try:
                statistic = self.reading_statistic_interactor.get_all_statistics_by_book(book_id)
            except BookDoesNotExist as exception:
                return self._create_response_for_exception(exception)
            serialized_statistic = ReadingStatisticDTOSerializer(statistic, many=True)

        else:
            statistic = self.reading_statistic_interactor.get_all_statistics_dto()

            serialized_statistic = ReadingStatisticDTOSerializer(statistic, many=True)

        return Response({'statistic': serialized_statistic.data}, status=status.HTTP_201_CREATED)
