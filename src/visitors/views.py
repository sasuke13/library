from django.conf import settings
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from core.base_api import ApiBaseView
from core.containers import VisitorContainer
from visitors.dto import VisitorRegistrationDTO
from visitors.exceptions import PasswordIsInvalid, VisitorAlreadyExists
from visitors.serializers import CookieTokenRefreshSerializer, VisitorDTOSerializer, VisitorRegistrationDTOSerializer


def logout(request, message: str):

    """
        Logouts logged user and deletes refresh token from cookies.

        Returns exception if refresh token was not given into the cookies.
    """

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

    return Response({'error': 'Refresh token not found'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView, ApiBaseView):
    """
        Implements logic of logout func.

        Gives message for the successful logout response.

        User have to be logged in to use this endpoint.
    """
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        message = "User was successfully logged out"
        return logout(request, message)


class CookieTokenObtainPairView(TokenObtainPairView):
    """
        Logins user giving the access token in response or
        returns that user's credentials are wrong.

        Saves refresh token into cookies.
    """

    parser_classes = (MultiPartParser, FormParser, JSONParser)

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
    """
        Refreshes the access token, taking the refresh token from cookies
    """

    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)

    serializer_class = CookieTokenRefreshSerializer


class VisitorRegistrationApiView(APIView, ApiBaseView):
    """
        Registers user into DB.

        Returns created user or PasswordIsInvalid if password is not safe enough
        whether VisitorAlreadyExists if the given email is already taken by another user.
    """

    parser_classes = (MultiPartParser, FormParser, JSONParser)
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
