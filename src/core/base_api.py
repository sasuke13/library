from rest_framework import status
from rest_framework.response import Response


class ApiBaseView:
    def _create_response_for_invalid_serializers(self, *serializers):
        errors = {}
        for serializer in serializers:
            if isinstance(serializer, type):
                serializer_instance = serializer(data=self.request.data)
            else:
                serializer_instance = serializer
            serializer_instance.is_valid()
            serializer_errors = serializer_instance.errors
            if serializer_errors:
                errors.update(serializer_errors)
            print(errors)
        return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

    def _create_response_for_exception(self, exception):
        exception = exception.message if type(exception.message) is not list else ''.join(exception.message)
        return Response({"error": str(exception)}, status=status.HTTP_400_BAD_REQUEST)

    def _create_response_not_found(self, exception):
        exception = exception.message if type(exception.message) is not list else ''.join(exception.message)
        return Response({"error": str(exception)}, status=status.HTTP_404_NOT_FOUND)
