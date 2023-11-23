from django.core.exceptions import ValidationError


class BookIsAlreadyTaken(ValidationError):
    def __init__(self, message='This book is already taken', *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.message = message or []


class SessionDoesNotExist(ValidationError):
    def __init__(self, message='You have no active sessions yet', *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.message = message or []


class StatisticDoesNotExist(ValidationError):
    def __init__(self, message='You have no statistic yet', *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.message = message or []
