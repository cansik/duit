from duit.annotation.Annotation import Annotation
from duit.model.DataField import DataField


class AnnotationList(Annotation):

    def __init__(self, *annotations: Annotation):
        self.annotations = annotations

    def __ror__(self, model: DataField) -> DataField:
        for annotation in self.annotations:
            model |= annotation
        return model
