from auto_dataclass.dj_model_to_dataclass import FromOrmToDataclass
from dependency_injector import containers, providers

from visitors.interactors import VisitorInteractor
from visitors.repositories import VisitorRepository
from visitors.services import VisitorService


class ToDTOContainer(containers.DeclarativeContainer):
    from_queryset_to_dto =providers.Factory(FromOrmToDataclass)


class Repositories(containers.DeclarativeContainer):
    visitor_repository = providers.Factory(
        VisitorRepository,
        converter=ToDTOContainer.from_queryset_to_dto
    )


class Services(containers.DeclarativeContainer):
    visitor_service = providers.Factory(
        VisitorService,
        repository=Repositories.visitor_repository
    )


class Interactors(containers.DeclarativeContainer):
    visitor_interactors = providers.Factory(
        VisitorInteractor,
        service=Services.visitor_service
    )


class VisitorContainer(containers.DeclarativeContainer):
    repository = Repositories.visitor_repository
    service = Services.visitor_service
    interactor = Interactors.visitor_interactors
