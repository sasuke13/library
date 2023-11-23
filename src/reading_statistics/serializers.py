from rest_framework import serializers

from books.serializers import BookDetailedViewDTOSerializer, BookWithTotalReadingTimeDTOSerializer
from visitors.serializers import VisitorDTOSerializer


class ReadingStatisticDTOSerializer(serializers.Serializer):
    book = BookDetailedViewDTOSerializer()
    visitor = VisitorDTOSerializer()
    total_reading_time = serializers.DurationField()


class ReadingStatisticWithBookTotalReadingTimeDTOSerializer(serializers.Serializer):
    book = BookWithTotalReadingTimeDTOSerializer()
    visitor = VisitorDTOSerializer()
    total_reading_time = serializers.DurationField()
