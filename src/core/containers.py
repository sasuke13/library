from auto_dataclass.dj_model_to_dataclass import FromOrmToDataclass
from dependency_injector import containers, providers

from books.interactors import BookInteractor
from books.repositories import BookRepository
from books.services import BookService
from visitors.interactors import VisitorInteractor, SessionInteractor
from visitors.repositories import VisitorRepositoryAndService, SessionRepository
from visitors.services import VisitorServiceAndService, SessionService


class ToDTOContainer(containers.DeclarativeContainer):
    from_queryset_to_dto = providers.Factory(FromOrmToDataclass)


class RepositoryContainer(containers.DeclarativeContainer):
    visitor_repository = providers.Factory(
        VisitorRepositoryAndService,
        converter=ToDTOContainer.from_queryset_to_dto
    )

    book_repository = providers.Factory(
        BookRepository,
        converter=ToDTOContainer.from_queryset_to_dto
    )

    session_repository = providers.Factory(
        SessionRepository,
        converter=ToDTOContainer.from_queryset_to_dto
    )


class ServiceContainer(containers.DeclarativeContainer):
    visitor_service = providers.Factory(
        VisitorServiceAndService,
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


class InteractorContainer(containers.DeclarativeContainer):
    visitor_interactor = providers.Factory(
        VisitorInteractor,
        visitor_service=ServiceContainer.visitor_service,
        book_service=ServiceContainer.book_service
    )

    book_interactor = providers.Factory(
        BookInteractor,
        book_service=ServiceContainer.book_service
    )

    session_interface = providers.Factory(
        SessionInteractor,
        session_service=ServiceContainer.session_service,
        book_service=ServiceContainer.book_service
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
    interactor = InteractorContainer.session_interface
