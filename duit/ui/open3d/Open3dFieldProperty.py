from abc import ABC, abstractmethod
from typing import Optional, Iterable, Generic

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
        if self.hide_label:
            return gui.Label(""), self.create_field()

        label = gui.Label(f"{self.annotation.name}:")
        label.font_id = Open3dContext.OPEN3D_LABEL_FONT_ID
        return label, self.create_field()

    @abstractmethod
    def create_field(self) -> Widget:
        pass
