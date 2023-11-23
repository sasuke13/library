from django.core.exceptions import ValidationError


class StatisticDoesNotExist(ValidationError):
    def __init__(self, message='You have no statistic yet', *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.message = message or []
