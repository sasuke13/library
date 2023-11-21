from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from books.serializers import BookDetailedViewDTOSerializer, BookListViewDTOSerializer
from core.base_api import ApiBaseView
from core.containers import BookContainer


class BookAPIVew(APIView, ApiBaseView):
    book_interactor = BookContainer.interactor()

    def get(self, request, book_id: int = None):
        if book_id:
            book = self.book_interactor.get_book_dto_by_id(book_id)

            serialized_book = BookDetailedViewDTOSerializer(book)

        else:
            book = self.book_interactor.get_all_books_dto()

            serialized_book = BookListViewDTOSerializer(book, many=True)

        return Response({'book': serialized_book.data}, status=status.HTTP_200_OK)
