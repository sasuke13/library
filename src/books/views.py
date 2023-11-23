from rest_framework import status
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from books.dto import CreateBookDTO
from books.exceptions import BookDoesNotExist
from books.serializers import BookDetailedViewDTOSerializer, BookListViewDTOSerializer, CreateBookDTOSerializer
from core.base_api import ApiBaseView
from core.containers import BookContainer


class BookAPIVew(APIView, ApiBaseView):
    """
        Accepts book id for Book detailed view.
        If book id was not provided, returns list of books.
    """
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    book_interactor = BookContainer.interactor()

    def get(self, request, book_id: int = None):
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

    def post(self, request):
        serialized_data = CreateBookDTOSerializer(data=request.data)

        is_serialized_data_valid = serialized_data.is_valid()

        if not is_serialized_data_valid:
            return self._create_response_for_invalid_serializers(CreateBookDTOSerializer)

        create_book_data = CreateBookDTO(**serialized_data.validated_data)

        created_book = self.book_interactor.create_book(create_book_data)

        serialized_created_book = BookDetailedViewDTOSerializer(created_book)

        return Response(
            {
                'message': 'Book was successfully created!',
                'book': serialized_created_book.data
            },
            status=status.HTTP_201_CREATED
        )
