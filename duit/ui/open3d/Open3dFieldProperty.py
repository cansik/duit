from abc import ABC, abstractmethod
from typing import Optional, Iterable, Generic, Sequence, Union

from open3d.visualization import gui
from open3d.visualization.gui import Widget

from duit.model.DataField import T
from duit.ui.BaseProperty import M
from duit.ui.annotations import UIAnnotation
from duit.ui.open3d import Open3dContext
from duit.ui.open3d.Open3dProperty import Open3dProperty


class Open3dFieldProperty(Generic[T, M], Open3dProperty[T, M], ABC):
    def __init__(self, annotation: UIAnnotation, model: Optional[M] = None,
                 hide_label: bool = False, raw_output: bool = False):
        """
        Initialize an Open3dFieldProperty.

        :param annotation: The UIAnnotation associated with this property.
        :param model: The data model for this property (default is None).
        :param hide_label: Whether to hide the label associated with the property (default is False).
        :param raw_output: Whether to return the raw output of the create_field method (default is False).
        """
        super().__init__(annotation, model)
        self.hide_label = hide_label
        self.raw_output = raw_output

    def create_widgets(self) -> Iterable[Widget]:
        """
        Create widgets for the Open3dFieldProperty.

        This method generates the widgets for the Open3dFieldProperty, including the label and the field.

        :return: An iterable of Open3D widgets.
        """
        fields = self.create_field()

        if not isinstance(fields, Sequence):
            fields = [fields]

        if self.hide_label:
            fields = gui.Label(""), *fields

        if self.hide_label or self.raw_output:
            return fields

        label = gui.Label(f"{self.annotation.name}:")
        label.font_id = Open3dContext.OPEN3D_LABEL_FONT_ID
        return label, *fields

    @abstractmethod
    def create_field(self) -> Union[Widget, Sequence[Widget]]:
        """
        Create the field widget for the Open3dFieldProperty.

        This method should be implemented in subclasses to create the specific field widget for the property.

        :return: The field widget or a sequence of field widgets.
        """
        pass
