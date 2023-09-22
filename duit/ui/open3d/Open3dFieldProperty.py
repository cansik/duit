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
    def __init__(self, annotation: UIAnnotation, model: Optional[M] = None, hide_label: bool = False):
        super().__init__(annotation, model)
        self.hide_label = hide_label

    def create_widgets(self) -> Iterable[Widget]:
        fields = self.create_field()

        if not isinstance(fields, Sequence):
            fields = [fields]

        if self.hide_label:
            return gui.Label(""), *fields

        label = gui.Label(f"{self.annotation.name}:")
        label.font_id = Open3dContext.OPEN3D_LABEL_FONT_ID
        return label, *fields

    @abstractmethod
    def create_field(self) -> Union[Widget, Sequence[Widget]]:
        pass
