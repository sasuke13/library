from django.core.exceptions import ValidationError


class PasswordIsInvalid(ValidationError):
    def __init__(self, message='This password is invalid', *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.message = message or []


class VisitorAlreadyExists(ValidationError):
    def __init__(self, message='This visitor already exist', *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.message = message or []


class SessionDoesNotExist(ValidationError):
    def __init__(self, message='You have no active sessions yet', *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.message = message or []
