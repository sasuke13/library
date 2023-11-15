from django.core.exceptions import ValidationError


class PasswordIsInvalid(ValidationError):
    def __init__(self, message="This password is invalid", *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.message = message or []
