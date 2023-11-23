from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from books.exceptions import BookDoesNotExist
from core.base_api import ApiBaseView
from core.containers import ReadingStatisticContainer
from reading_statistics.exceptions import StatisticDoesNotExist
from reading_statistics.serializers import (
    ReadingStatisticDTOSerializer,
    ReadingStatisticWithBookTotalReadingTimeDTOSerializer
)


class StatisticsAPIView(APIView, ApiBaseView):
    """
        Accepts book id and gets all book's statistics or returns
        BookDoesNotExist(book with that id does not exist) error message.
        If book was not provided, returns all statistics.
    """
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    reading_statistic_interactor = ReadingStatisticContainer.interactor()

    def get(self, request, book_id: int = None):
        if book_id:
            try:
                statistic = self.reading_statistic_interactor.get_all_statistics_dto_by_book(book_id)
            except BookDoesNotExist as exception:
                return self._create_response_not_found(exception)

        else:
            statistic = self.reading_statistic_interactor.get_all_statistics_dto()

        serialized_statistic = ReadingStatisticWithBookTotalReadingTimeDTOSerializer(statistic, many=True)

        return Response({'statistic': serialized_statistic.data}, status=status.HTTP_200_OK)


class VisitorStatisticsAPIView(APIView, ApiBaseView):
    """
        Accepts book id and gets visitor's statistic with the gotten book or
        returns BookDoesNotExist(book with provided id was not found),
        StatisticDoesNotExist(statistic does not exist) errors message.
        If book id was not provided, returns all visitor's statistic.
    """
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [IsAuthenticated]

    reading_statistic_interactor = ReadingStatisticContainer.interactor()

    def get(self, request, book_id: int = None):
        if book_id:
            try:
                statistic = (self.reading_statistic_interactor.
                             get_statistic_dto_by_visitor_and_book(request.user, book_id))

            except (BookDoesNotExist, StatisticDoesNotExist) as exception:
                return self._create_response_not_found(exception)

            serialized_statistic = ReadingStatisticDTOSerializer(statistic)

        else:
            statistic = self.reading_statistic_interactor.get_all_statistics_dto_by_visitor(request.user)

            serialized_statistic = ReadingStatisticDTOSerializer(statistic, many=True)

        return Response({'statistic': serialized_statistic.data}, status=status.HTTP_200_OK)
