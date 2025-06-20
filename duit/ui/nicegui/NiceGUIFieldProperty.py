from abc import ABC, abstractmethod
from typing import Generic, Optional, Iterable, Sequence

from nicegui import ui
from nicegui.element import Element

from duit.model.DataField import T
from duit.ui.BaseProperty import M
from duit.ui.annotations import UIAnnotation
from duit.ui.nicegui.NiceGUIProperty import NiceGUIProperty


class NiceGUIFieldProperty(Generic[T, M], NiceGUIProperty[T, M], ABC):
    """
    A base class for defining NiceGUI properties with associated UI annotations.

    This class handles the creation and management of NiceGUI elements linked to a specific property of a model.
    """

    def __init__(self, annotation: UIAnnotation, model: Optional[M] = None, hide_label: bool = False):
        """
        Initializes a NiceGUIFieldProperty.

        Args:
            annotation (UIAnnotation): The UI annotation associated with this property.
            model (Optional[M], optional): The model to link with the property. Defaults to None.
            hide_label (bool, optional): Whether to hide the label. Defaults to False.
        """
        super().__init__(annotation, model)
        self.hide_label = hide_label

        # defines style of properties
        self._default_props = "rounded outlined dense"

    def create_widgets(self) -> Iterable[Element]:
        """
        Creates NiceGUI elements for this property.

        Returns:
            Iterable[Element]: An iterable of NiceGUI elements.
        """
        if not self.hide_label:
            label = ui.markdown(f"{self.annotation.name}:").classes("p-1")
        result = self.create_field()

        if isinstance(result, Sequence):
            return result

        if self.hide_label:
            return [result]

        return label, result

    @abstractmethod
    def create_field(self) -> Element:
        """
        Creates the specific field widget for this property.

        Returns:
            Element: The field widget.
        """
        pass
