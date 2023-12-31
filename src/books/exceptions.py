from django.core.exceptions import ValidationError


class BookDoesNotExist(ValidationError):
    def __init__(self, message="Book does not exist", *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.message = message or []


class BookIsAlreadyTaken(ValidationError):
    def __init__(self, message='This book is already taken', *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.message = message or []
