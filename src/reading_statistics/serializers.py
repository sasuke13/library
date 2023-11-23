from rest_framework import serializers

from books.serializers import BookDetailedViewDTOSerializer
from visitors.serializers import VisitorDTOSerializer


class ReadingStatisticDTOSerializer(serializers.Serializer):
    book = BookDetailedViewDTOSerializer()
    visitor = VisitorDTOSerializer()
    total_reading_time = serializers.DurationField()