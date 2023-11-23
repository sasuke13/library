from rest_framework import serializers

from books.serializers import BookDetailedViewDTOSerializer
from visitors.serializers import VisitorDTOSerializer


class SessionDTOSerializer(serializers.Serializer):
    book = BookDetailedViewDTOSerializer()
    visitor = VisitorDTOSerializer()
    session_start = serializers.DateTimeField()
    session_end = serializers.DateTimeField()
    is_active = serializers.BooleanField()
