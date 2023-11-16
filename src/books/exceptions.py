from django.core.exceptions import ValidationError


class BookDoesNotExist(ValidationError):
    def __init__(self, message="Book does not exist", *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.message = message or []
