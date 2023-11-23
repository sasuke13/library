from rest_framework import serializers

from books.serializers import BookDetailedViewDTOSerializer
from visitors.serializers import VisitorDTOSerializer


class ReadingStatisticDTOSerializer(serializers.Serializer):
    book = BookDetailedViewDTOSerializer()
    visitor = VisitorDTOSerializer()
    total_reading_time = serializers.DurationField()


class SessionDTOSerializer(serializers.Serializer):
    book = BookDetailedViewDTOSerializer()
    visitor = VisitorDTOSerializer()
    session_start = serializers.DateTimeField()
    session_end = serializers.DateTimeField()
    is_active = serializers.BooleanField()


class SessionAndTotalReadingTimeDTOSerializer(serializers.Serializer):
    session = SessionDTOSerializer()
    statistic = ReadingStatisticDTOSerializer()
