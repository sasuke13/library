from rest_framework import serializers


class BookDetailedViewDTOSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=32)
    author = serializers.CharField(max_length=50)
    year_of_publication = serializers.IntegerField()
    short_about = serializers.CharField(max_length=128)
    about = serializers.CharField(max_length=512)
    last_used = serializers.DateTimeField(allow_null=True)
