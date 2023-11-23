from rest_framework.exceptions import ValidationError


class SessionDoesNotExist(ValidationError):
    def __init__(self, message='You have no active reading_sessions yet', *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.message = message or []
