from duit.annotation.Annotation import Annotation
from duit.model.DataField import DataField


class AnnotationList(Annotation):
    """
    A composite annotation class that combines multiple annotations.

    Args:
        *annotations (List[Annotation]): Variable number of annotations to be combined.

    Attributes:
        annotations (Tuple[Annotation]): A tuple containing the annotations to be combined.
    """

    def __init__(self, *annotations: Annotation):
        """
        Initialize an AnnotationList instance with the provided annotations.

        Args:
            *annotations (Annotation): Variable number of annotations to be combined.
        """
        self.annotations = annotations

    def _apply_annotation(self, model: DataField) -> DataField:
        """
        Apply the combined annotations to a DataField model.

        Args:
            model (DataField): The DataField model to apply the annotations to.

        Returns:
            DataField: The modified DataField model with the combined annotations applied.
        """
        for annotation in self.annotations:
            model |= annotation
        return model

    @staticmethod
    def _get_annotation_attribute_name() -> str:
        """
        Get the name of the annotation attribute.

        This method raises an Exception since AnnotationList is not a real Annotation.

        Returns:
            str: The name of the annotation attribute (raises Exception).
        """
        raise Exception("AnnotationList is not a real Annotation.")
