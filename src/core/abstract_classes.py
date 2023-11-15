from auto_dataclass.dj_model_to_dataclass import ToDTOConverter


class AbstractRepository:
    def __init__(self, converter: ToDTOConverter):
        self.converter = converter
