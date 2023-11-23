from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class BookDetailedViewDTOSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=32)
    author = serializers.CharField(max_length=50)
    year_of_publication = serializers.IntegerField()
    short_about = serializers.CharField(max_length=128)
    about = serializers.CharField(max_length=512)
    last_used = serializers.DateTimeField(allow_null=True)


class CreateBookDTOSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=32)
    author = serializers.CharField(max_length=50)
    year_of_publication = serializers.IntegerField()
    short_about = serializers.CharField(max_length=128)
    about = serializers.CharField(max_length=512)

    def validate(self, attrs):
        current_year = datetime.now().year

        if 0 <= attrs['year_of_publication'] <= current_year:
            return super().validate(attrs)
        else:
            raise ValidationError('Invalid year of publication')


class BookListViewDTOSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=32)
    author = serializers.CharField(max_length=50)
    year_of_publication = serializers.IntegerField()
    short_about = serializers.CharField(max_length=128)


class BookWithTotalReadingTimeDTOSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    total_reading_time = serializers.DurationField()
