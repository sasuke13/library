from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from books.exceptions import BookDoesNotExist
from core.base_api import ApiBaseView
from core.containers import ReadingStatisticContainer
from reading_statistics.exceptions import StatisticDoesNotExist
from reading_statistics.serializers import ReadingStatisticDTOSerializer


class StatisticsAPIView(APIView, ApiBaseView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    reading_statistic_interactor = ReadingStatisticContainer.interactor()

    def get(self, request, book_id: int = None):
        if book_id:
            try:
                statistic = self.reading_statistic_interactor.get_all_statistics_dto_by_book(book_id)
            except BookDoesNotExist as exception:
                return self._create_response_for_exception(exception)
            serialized_statistic = ReadingStatisticDTOSerializer(statistic, many=True)

        else:
            statistic = self.reading_statistic_interactor.get_all_statistics_dto()

            serialized_statistic = ReadingStatisticDTOSerializer(statistic, many=True)

        return Response({'statistic': serialized_statistic.data}, status=status.HTTP_200_OK)


class VisitorStatisticsAPIView(APIView, ApiBaseView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [IsAuthenticated]

    reading_statistic_interactor = ReadingStatisticContainer.interactor()

    def get(self, request, book_id: int = None):
        if book_id:
            try:
                statistic = (self.reading_statistic_interactor.
                             get_statistic_dto_by_visitor_and_book(request.user, book_id))

            except (BookDoesNotExist, StatisticDoesNotExist) as exception:
                return self._create_response_for_exception(exception)

            serialized_statistic = ReadingStatisticDTOSerializer(statistic)

        else:
            statistic = self.reading_statistic_interactor.get_all_statistics_dto_by_visitor(request.user)

            serialized_statistic = ReadingStatisticDTOSerializer(statistic, many=True)

        return Response({'statistic': serialized_statistic.data}, status=status.HTTP_200_OK)
