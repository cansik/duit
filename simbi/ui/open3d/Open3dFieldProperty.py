from abc import ABC, abstractmethod
from typing import Optional, Iterable, Generic

from open3d.visualization import gui
from open3d.visualization.gui import Widget

from simbi.model.DataModel import DataModel, T
from simbi.ui.annotations import UIAnnotation
from simbi.ui.open3d.Open3dProperty import Open3dProperty


class Open3dFieldProperty(Generic[T], Open3dProperty[T], ABC):
    def __init__(self, annotation: UIAnnotation, model: Optional[DataModel] = None):
        super().__init__(annotation, model)

    def create_widgets(self) -> Iterable[Widget]:
        return gui.Label(f"{self.annotation.name}:"), self.create_field()

    @abstractmethod
    def create_field(self) -> Widget:
        pass
