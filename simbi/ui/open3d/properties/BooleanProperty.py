from functools import partial
from typing import Optional

from open3d.cpu.pybind.visualization.gui import Widget
from open3d.visualization import gui

from simbi.model.DataModel import DataModel
from simbi.ui.annotations.BooleanAnnotation import BooleanAnnotation
from simbi.ui.open3d.Open3dFieldProperty import Open3dFieldProperty


class BooleanProperty(Open3dFieldProperty[BooleanAnnotation]):
    def __init__(self, annotation: BooleanAnnotation, model: Optional[DataModel] = None):
        super().__init__(annotation, model)

    def create_field(self) -> Widget:
        field = gui.Checkbox("")

        def on_dm_changed(value, f: gui.Checkbox):
            f.checked = value

        def on_ui_changed(value, m: DataModel):
            m.value = value

        self.model.on_changed.append(partial(on_dm_changed, f=field))
        field.set_on_checked(partial(on_ui_changed, m=self.model))

        self.model.fire_latest()
        return field
