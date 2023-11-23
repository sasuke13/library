from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from books.exceptions import BookDoesNotExist, BookIsAlreadyTaken
from core.base_api import ApiBaseView
from core.containers import SessionContainer
from reading_sessions.exceptions import SessionDoesNotExist
from reading_sessions.serializers import SessionDTOSerializer


class SessionAPIView(APIView, ApiBaseView):
    """
        GET:
            Returns visitor's active session
            or returns that visitor have no active session.

        POST:
            Accepts book id and opens session or returns
            BookDoesNotExist(book with provided id does not exist),
            BookIsAlreadyTaken(book was already taken and unavailable) errors messages
    """
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [IsAuthenticated]

    session_interactor = SessionContainer.interactor()

    def get(self, request):
        try:
            session = self.session_interactor.get_active_session_dto_by_visitor(request.user)
        except SessionDoesNotExist as exception:
            return self._create_response_not_found(exception)

        serialized_session = SessionDTOSerializer(session)

        return Response({'session': serialized_session.data}, status=status.HTTP_200_OK)

    def post(self, request, book_id: int):
        try:
            session = self.session_interactor.open_session(self.request.user, book_id)

        except (BookDoesNotExist, BookIsAlreadyTaken) as exception:
            return self._create_response_for_exception(exception)

        serialized_session = SessionDTOSerializer(session)

        return Response({
            'message': 'Session has been successfully opened!',
            'session': serialized_session.data
        }, status=status.HTTP_201_CREATED)


class CloseSessionAPIView(APIView, ApiBaseView):
    """
        Closes visitor's active session or
        raises SessionDoesNotExist(visitor have no active sessions) error
    """
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [IsAuthenticated]

    session_interactor = SessionContainer.interactor()

    def post(self, request):
        try:
            message = self.session_interactor.close_session(request.user)
        except SessionDoesNotExist as exception:
            return self._create_response_not_found(exception)

        return Response({'message': message}, status=status.HTTP_200_OK)
