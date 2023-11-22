from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from books.exceptions import BookDoesNotExist
from books.serializers import BookDetailedViewDTOSerializer, BookListViewDTOSerializer
from core.base_api import ApiBaseView
from core.containers import BookContainer
from core.tasks import debug_task


class BookAPIVew(APIView, ApiBaseView):
    book_interactor = BookContainer.interactor()

    def get(self, request, book_id: int = None):
        debug_task.delay()
        if book_id:
            try:
                book = self.book_interactor.get_book_dto_by_id(book_id)

            except BookDoesNotExist as exception:
                return self._create_response_not_found(exception)

            serialized_book = BookDetailedViewDTOSerializer(book)

        else:
            book = self.book_interactor.get_all_books_dto()

            serialized_book = BookListViewDTOSerializer(book, many=True)

        return Response({'book': serialized_book.data}, status=status.HTTP_200_OK)
