from abc import ABC, abstractmethod
from typing import TypeVar

from duit.model.DataField import DataField

M = TypeVar("M", bound=DataField)


class Annotation(ABC):
    """An abstract base class for annotations."""

    def __ror__(self, model: M) -> M:
        """
        Apply the annotation to a model.

        Args:
            model (M): The model to apply the annotation to.

        Returns:
            M: The modified model with the annotation applied.
        """
        return self._apply_annotation(model)

    @abstractmethod
    def _apply_annotation(self, model: M) -> M:
        """
        Apply the annotation to a model.

        Args:
            model (M): The model to apply the annotation to.

        Returns:
            M: The modified model with the annotation applied.
        """
        pass

    @staticmethod
    @abstractmethod
    def _get_annotation_attribute_name() -> str:
        """
        Get the name of the annotation attribute.

        This method is used to retrieve the name of the annotation attribute that stores the annotation data.

        Returns:
            str: The name of the annotation attribute.
        """
        pass
