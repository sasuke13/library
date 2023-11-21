from auto_dataclass.dj_model_to_dataclass import FromOrmToDataclass
from dependency_injector import containers, providers

from books.interactors import BookInteractor
from books.repositories import BookRepository
from books.services import BookService
from visitors.interactors import VisitorInteractor, SessionInteractor, ReadingStatisticInteractor
from visitors.repositories import VisitorRepository, SessionRepository, DTOConverterRepository, \
    ReadingStatisticRepository
from visitors.services import VisitorService, SessionService, DTOConverterService, ReadingStatisticService


class ToDTOContainer(containers.DeclarativeContainer):
    from_queryset_to_dto = providers.Factory(FromOrmToDataclass)


class RepositoryContainer(containers.DeclarativeContainer):
    visitor_repository = providers.Factory(
        VisitorRepository,
    )

    book_repository = providers.Factory(
        BookRepository,
    )

    session_repository = providers.Factory(
        SessionRepository,
    )

    reading_statistic_repository = providers.Factory(
        ReadingStatisticRepository
    )

    dto_converter_repository = providers.Factory(
        DTOConverterRepository,
        converter=ToDTOContainer.from_queryset_to_dto
    )


class ServiceContainer(containers.DeclarativeContainer):
    visitor_service = providers.Factory(
        VisitorService,
        visitor_repository=RepositoryContainer.visitor_repository
    )

    book_service = providers.Factory(
        BookService,
        book_repository=RepositoryContainer.book_repository
    )

    session_service = providers.Factory(
        SessionService,
        session_repository=RepositoryContainer.session_repository
    )

    reading_statistic_service = providers.Factory(
        ReadingStatisticService,
        reading_statistic_repository=RepositoryContainer.reading_statistic_repository
    )

    dto_converter_service = providers.Factory(
        DTOConverterService,
        converter_repository=RepositoryContainer.dto_converter_repository
    )


class InteractorContainer(containers.DeclarativeContainer):
    visitor_interactor = providers.Factory(
        VisitorInteractor,
        visitor_service=ServiceContainer.visitor_service,
        book_service=ServiceContainer.book_service,
        converter_service=ServiceContainer.dto_converter_service
    )

    book_interactor = providers.Factory(
        BookInteractor,
        book_service=ServiceContainer.book_service,
        converter_service=ServiceContainer.dto_converter_service
    )

    session_interactor = providers.Factory(
        SessionInteractor,
        visitor_service=ServiceContainer.visitor_service,
        session_service=ServiceContainer.session_service,
        book_service=ServiceContainer.book_service,
        reading_statistic_service=ServiceContainer.reading_statistic_service,
        converter_service=ServiceContainer.dto_converter_service
    )

    reading_statistic_interactor = providers.Factory(
        ReadingStatisticInteractor,
        reading_statistic_service=ServiceContainer.reading_statistic_service,
        converter_service=ServiceContainer.dto_converter_service,
        session_service=ServiceContainer.session_service,
        book_service=ServiceContainer.book_service,
    )


class VisitorContainer(containers.DeclarativeContainer):
    repository = RepositoryContainer.visitor_repository
    service = ServiceContainer.visitor_service
    interactor = InteractorContainer.visitor_interactor


class BookContainer(containers.DeclarativeContainer):
    repository = RepositoryContainer.book_repository
    service = ServiceContainer.book_service
    interactor = InteractorContainer.book_interactor


class SessionContainer(containers.DeclarativeContainer):
    repository = RepositoryContainer.session_repository
    service = ServiceContainer.session_service
    interactor = InteractorContainer.session_interactor


class ReadingStatisticContainer(containers.DeclarativeContainer):
    repository = RepositoryContainer.reading_statistic_repository
    service = ServiceContainer.reading_statistic_service
    interactor = InteractorContainer.reading_statistic_interactor
