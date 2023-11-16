from rest_framework import serializers
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from books.serializers import BookDetailedViewDTOSerializer


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid token found in cookie')


class VisitorRegistrationDTOSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)
    name = serializers.CharField(max_length=32)
    surname = serializers.CharField(max_length=32)


class VisitorDTOSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=32)
    surname = serializers.CharField(max_length=32)
    total_reading_time = serializers.TimeField()


class ReadingStatisticDTOSerializer(serializers.Serializer):
    book = BookDetailedViewDTOSerializer()
    visitor = VisitorDTOSerializer()
    total_reading_time = serializers.TimeField()


class SessionDTOSerializer(serializers.Serializer):
    book = BookDetailedViewDTOSerializer()
    visitor = VisitorDTOSerializer()
    session_start = serializers.DateTimeField()
    session_end = serializers.DateTimeField()
    is_active = serializers.BooleanField()
