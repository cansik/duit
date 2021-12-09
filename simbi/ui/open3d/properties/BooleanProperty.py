from typing import Optional

from open3d.cpu.pybind.visualization.gui import Widget
from open3d.visualization import gui

from simbi.model.DataField import DataField
from simbi.ui.annotations.BooleanAnnotation import BooleanAnnotation
from simbi.ui.open3d.Open3dFieldProperty import Open3dFieldProperty


class BooleanProperty(Open3dFieldProperty[BooleanAnnotation]):
    def __init__(self, annotation: BooleanAnnotation, model: Optional[DataField] = None):
        super().__init__(annotation, model)

    def create_field(self) -> Widget:
        field = gui.Checkbox("")

        def on_dm_changed(value):
            field.checked = value

        def on_ui_changed(value):
            self.model.value = value

        self.model.on_changed.append(on_dm_changed)
        field.set_on_checked(on_ui_changed)

        self.model.fire_latest()
        return field
